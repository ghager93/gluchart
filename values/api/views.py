import csv
import copy
from io import TextIOWrapper
from datetime import datetime, timedelta


from rest_framework import views, viewsets, permissions, response, status

from chart.models import GlucoseValue
from chart.filters import GlucoseValueFilter, VariablePagination
from .serializers import GlucoseValueSerializer, GlucoseValueDebugSerializer

class GlucoseValueViewSet(viewsets.ModelViewSet):
    serializer_list_class = GlucoseValueSerializer
    serializer_create_class = GlucoseValueDebugSerializer
    debug_serializer_class = GlucoseValueDebugSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = GlucoseValueFilter
    pagination_class = VariablePagination

    def get_queryset(self):
        return GlucoseValue.objects.filter(user=self.request.user).order_by('timestamp')

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            return self.bulk_create(request, *args, **kwargs)
        request_data = self.add_user_if_not_exist(request.data, request.user.id)
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def bulk_create(self, request, *args, **kwargs):
        request_data = list(map(lambda entry: self.add_user_if_not_exist(entry, request.user.id), request.data))
        return self.do_bulk_create(request_data)
    
    def do_bulk_create(self, data):
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)  

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            if "fill" in request.query_params:
                data = self._fill_null_values(data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_serializer_class(self):
        if "debug" in self.request.query_params:
            return self.debug_serializer_class
        if self.action == "list":
            return self.serializer_list_class
        return self.serializer_create_class

    def _fill_null_values(self, data):
        def ts_diff(ts1, ts2):
            dt1 = datetime.strptime(ts1, "%Y-%m-%dT%H:%M:%SZ")
            dt2 = datetime.strptime(ts2, "%Y-%m-%dT%H:%M:%SZ")

            return dt1 - dt2

        if len(data) < 2:
            return data
        
        new_values = [data[0]]
        left_values = data[:-1]
        right_values = data[1:]
        deltas = [ts_diff(right_values[i]["timestamp"], left_values[i]["timestamp"]) for i in range(len(left_values))]
        for i, delta in enumerate(deltas):
            num_nulls = delta // timedelta(minutes=15)
            if num_nulls * timedelta(minutes=15) == delta:
                num_nulls -= 1
            for j in range(num_nulls):
                new_value = copy.deepcopy(data[i])
                new_value["value"] = None
                new_dt = datetime.strptime(new_value["timestamp"], "%Y-%m-%dT%H:%M:%SZ") + (j+1)*timedelta(minutes=15)
                new_value["timestamp"] = datetime.strftime(new_dt, "%Y-%m-%dT%H:%M:%SZ")
                new_values.append(new_value)
            new_values.append(data[i+1])
        
        return new_values
        
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




