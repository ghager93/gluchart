import csv
import math
from io import TextIOWrapper
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import permissions, viewsets, views, response, status
from django_filters.rest_framework import DjangoFilterBackend

from . import librelinkup
from .models import Source, GlucoseValue
from .serializers import UserSerializer, SourceSerializer, GlucoseValueSerializer
from .filters import GlucoseValueFilter, SourceFilter
from .forms import LibreLinkUp
from .utils import round_timestamp


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by('name')
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SourceFilter

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        if request.htmx:
            response.status_code = 200

        return response
    

class GlucoseValueViewSet(viewsets.ModelViewSet):
    queryset = GlucoseValue.objects.all().order_by('timestamp')
    serializer_class = GlucoseValueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GlucoseValueFilter

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            return self.bulk_create(request, *args, **kwargs)
        if "user" not in request.data.keys():
            request.data["user"] = request.user.id
        return super().create(request, *args, **kwargs)

    def bulk_create(self, request, *args, **kwargs):
        request_data = list(map(lambda entry: self.add_user_if_not_exist(entry, request.user.id), request.data))
        return self.do_bulk_create(request_data)
    
    def do_bulk_create(self, data):
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)        
    
    @staticmethod
    def add_user_if_not_exist(entry, user_id):
        if "user" not in entry.keys():
            entry["user"] = user_id
        return entry

class GlucoseValueBatchCreate(views.APIView):
    queryset = GlucoseValue.objects.all()

    def post(self, request):
        try:
            file_obj = request.FILES['csv_file']

            if not is_csv_type(file_obj):
                raise Exception("Invalid file format")
            
            if not is_csv_size_okay(file_obj):
                raise Exception("File size exceeds allowed limit.")
            
            text_file = TextIOWrapper(file_obj.file, encoding='utf-8')
            csv_reader = csv.reader(text_file)
            
            # Process each row in the CSV file
            bulk_create_objs = [GlucoseValue(value=row[1], time_of_reading=row[0]) for row in csv_reader]
            GlucoseValue.objects.bulk_create(bulk_create_objs)
            
            return response.Response(f"{len(bulk_create_objs)} values added.", status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    

def is_csv_type(file_obj):
    return file_obj.content_type.startswith('text')
    

def is_csv_size_okay(file_obj):
    MAX_CSV_FILE_SIZE_MB = 5
    return file_obj.size <= MAX_CSV_FILE_SIZE_MB * 1024 * 1024


class GraphView(views.View):
    template_name = 'graph.html'
    max_readings = 400

    def get(self, request):
        n_readings = min(self.max_readings, GlucoseValue.objects.filter(user=request.user.id).count())
        values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:n_readings]
        timestamps = [value.time_of_reading.isoformat() for value in values]
        readings = [float(v.value) if v.value else None for v in values]
        if values[0] and values[1]:
            arrow_angle = -int(math.degrees(math.atan(float(values[0].value) - float(values[1].value))))
        else:
            arrow_angle = 0
        return render(request, self.template_name, {
            "x_values": f"{timestamps}",
            "y_values": f"{readings}".replace("None", "").replace("\'", "").replace("\"", ""),
            "x_range_min": (values[0].time_of_reading - timedelta(hours=2)).isoformat(), 
            "x_range_max": values[0].time_of_reading.isoformat(),
            "last_reading": values[0].value,
            "arrow_angle": arrow_angle,
        })
    

class DataSourceView(views.View):
    template_name = 'data_sources.html'
    def get(self, request):
        sources = Source.objects.filter(user=request.user).order_by("created_at")

        return render(request, self.template_name, {
            "sources": sources
        })


class AddDataSourceView(views.View):
    template_name = 'add_data_source.html'
    def get(self, request):
        form = LibreLinkUp()
        return render(request, self.template_name, {
            "form": form
        })
    
    def post(self, request):
        form = LibreLinkUp(request.POST)
        if form.is_valid():
            token, token_expiry = librelinkup.get_token(form.cleaned_data["email"], form.cleaned_data["password"])
            patient_id = librelinkup.get_patient_id(token)
            sensor_start, graph_data = librelinkup.get_device_info(token, patient_id)

            cache_data = {
                "name": form.cleaned_data["name"],
                "token": token,
                "token_expiry": token_expiry,
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
                "patient_id": patient_id,
                "sensor_start": sensor_start,
                "graph_data": graph_data,
            }

            cache_key = f"new_source_{request.session.session_key}"
            cache.set(cache_key, cache_data, timeout=3600)
            
            return render(request, "data_source_found.html")
        

def add_new_source(request):
    cache_key = f"new_source_{request.session.session_key}"
    data = cache.get(cache_key)

    new_source = Source(
        name=data["name"],
        type="libre_link_up",
        token=data["token"],
        token_expiry=datetime.fromtimestamp(int(data["token_expiry"])),
        email=data["email"],
        password=data["password"],
        patient_id=data["patient_id"],
        sensor_start=datetime.fromtimestamp(int(data["sensor_start"])),
        user=User.objects.get(id=request.user.id)
    )
    new_source.save()

    values = []
    for entry in data["graph_data"]:
        entry["user"] = request.user
        entry["source"] = new_source
        entry["time_of_reading"] = _llu_datetime(entry["timestamp"])
        value = GlucoseValue(**entry)
        value.save()
        values.append(value)

    return redirect("graph")


def _llu_datetime(timestamp):
    return datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")


def get_llu_data(request):
    for source in Source.objects.filter(user=request.user, type="libre_link_up"):
        try:
            _, graph_data = librelinkup.get_device_info(source.token, source.patient_id)
        
            values = []
            for entry in graph_data:
                entry["user"] = request.user
                entry["source"] = source
                entry["time_of_reading"] = _llu_datetime(entry["timestamp"])
                value = GlucoseValue(**entry)
                value.save()
                values.append(value)
        except:
            pass
        
    return redirect("graph")


    
class EntriesView(views.View):
    def get(self, request):
        return HttpResponse(GlucoseValue.objects.filter(time_of_reading__lt="2020-01-06T00:00:00Z").values('time_of_reading', 'value'))
    






    

