from rest_framework import serializers

from chart.models import GlucoseValue


class GlucoseValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseValue
        fields = ['value', 'timestamp']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.query_params.get('fill'):
            data = self._fill_null_values(data)
        return data


class GlucoseValueDebugSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseValue
        fields = '__all__'