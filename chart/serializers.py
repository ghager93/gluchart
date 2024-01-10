from django.contrib.auth.models import User
from rest_framework import serializers

from models import Source, GlucoseValue


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class GlucoseValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseValue
        fields = '__all__'