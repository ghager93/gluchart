from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from .models import Source, GlucoseValue
from .serializers import UserSerializer, SourceSerializer, GlucoseValueSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by('name')
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class GlucoseValueViewSet(viewsets.ModelViewSet):
    queryset = GlucoseValue.objects.all().order_by('time_of_reading')
    serializer_class = GlucoseValueSerializer
    permission_classes = [permissions.IsAuthenticated]
