from django_filters import rest_framework as filters
from rest_framework import pagination
from .models import GlucoseValue, Source

class GlucoseValueFilter(filters.FilterSet):
    start_dt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_dt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lt")
    value_min = filters.NumberFilter(field_name="value", lookup_expr="gte")
    value_max = filters.NumberFilter(field_name="value", lookup_expr="lt")

    order = filters.OrderingFilter(
        fields=["timestamp"],
    )

    class Meta:
        model = GlucoseValue
        fields = ["value", "timestamp", "source"]


class SourceFilter(filters.FilterSet):
    class Meta: 
        model = Source
        fields = ["name", "type"]


class VariablePagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'