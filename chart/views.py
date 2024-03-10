import csv
from io import TextIOWrapper
from datetime import timedelta

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, views, response, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Source, GlucoseValue
from .serializers import UserSerializer, SourceSerializer, GlucoseValueSerializer
from .filters import GlucoseValueFilter, SourceFilter


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

class GlucoseValueViewSet(viewsets.ModelViewSet):
    queryset = GlucoseValue.objects.all().order_by('time_of_reading')
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
        serializer = self.get_serializer(data=request_data, many=True)
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

    def get(self, request):
        values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:400]
        timestamps = [value.time_of_reading.isoformat() for value in values]
        readings = [float(value.value) for value in values]
        return render(request, self.template_name, {
            "x_values": f"{timestamps}",
            "y_values": f"{readings}".replace("None", "").replace("\'", "").replace("\"", ""),
            "x_range_min": (values[0].time_of_reading - timedelta(hours=2)).isoformat(), 
            "x_range_max": values[0].time_of_reading.isoformat()
        })
    

class EntriesView(views.View):
    def get(self, request):
        return HttpResponse(GlucoseValue.objects.filter(time_of_reading__lt="2020-01-06T00:00:00Z").values('time_of_reading', 'value'))
    






    

