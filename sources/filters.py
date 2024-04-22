from django_filters import rest_framework as filters
from rest_framework import pagination
from .models import Source


class SourceFilter(filters.FilterSet):
    class Meta: 
        model = Source
        fields = ["name", "type"]