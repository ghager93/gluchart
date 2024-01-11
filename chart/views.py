from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
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

    # def get_queryset(self):
    #     print(self.request.query_params)
    #     return GlucoseValue.objects.filter(value=3).order_by('time_of_reading')
