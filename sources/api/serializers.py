from rest_framework import serializers

from sources.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'