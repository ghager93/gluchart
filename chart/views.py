import csv

from io import TextIOWrapper
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
            for row in csv_reader:
                print(row)
            
            return response.Response("test", status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    

def is_csv_type(file_obj):
    return file_obj.content_type.startswith('text')
    

def is_csv_size_okay(file_obj):
    MAX_CSV_FILE_SIZE_MB = 5
    return file_obj.size <= MAX_CSV_FILE_SIZE_MB * 1024 * 1024
    

