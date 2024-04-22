from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from sources.models import Source
from sources.filters import SourceFilter
from .serializers import SourceSerializer


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