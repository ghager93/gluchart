from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    api_key = models.CharField(max_length=200)

    # Returns a default source for use as foreign key
    @classmethod
    def get_default_pk(cls):
        source, _ = cls.objects.get_or_create(
            name='NO_SOURCE',
            type='',
            api_key=''
        )
        return source


class GlucoseValue(models.Model):
    value = models.CharField(max_length=10)
    time_of_reading = models.DateTimeField()
    source = models.ForeignKey(to=Source, on_delete=models.SET_DEFAULT, default=Source.get_default_pk)


