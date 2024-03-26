from django_filters import rest_framework as filters

from .models import GlucoseValue, Source

class GlucoseValueFilter(filters.FilterSet):
    start_dt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_dt = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lt")
    value_min = filters.NumberFilter(field_name="value", lookup_expr="gte")
    value_max = filters.NumberFilter(field_name="value", lookup_expr="lt")

    class Meta:
        model = GlucoseValue
        fields = ["user", "value", "timestamp"]


class SourceFilter(filters.FilterSet):
    class Meta: 
        model = Source
        fields = ["name", "type"]