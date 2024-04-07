from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import constraints

class Source(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    token = models.CharField(max_length=500)
    token_expiry = models.DateTimeField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    patient_id = models.CharField(max_length=50)
    sensor_start = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    # Returns a default source for use as foreign key
    @classmethod
    def get_default_pk(cls):
        try:
            default_user = User.objects.get(username="admin")
        except ObjectDoesNotExist:
            default_user = User.objects.filter(is_superuser=True).first()
        
        source, _ = cls.objects.get_or_create(
            name='NO_SOURCE',
            type='',
            token='',
            user=default_user
        )
        return source
    
    class Meta:
        constraints = [
            # constraints.UniqueConstraint(fields=['type', 'patient_id'], name='unique_source')
        ]


class GlucoseValue(models.Model):
    value = models.CharField(max_length=10, null=True)
    time_of_reading = models.DateTimeField()
    timestamp = models.DateTimeField(editable=False)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.timestamp = self.time_of_reading.replace(second=0)
            try:
                existing_instance = GlucoseValue.objects.get(user=self.user, timestamp=self.timestamp)
                self.pk = existing_instance.pk
                self.created_at = existing_instance.created_at
            except GlucoseValue.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    class Meta: 
        indexes = [
            models.Index(fields=['user', 'timestamp'])
        ]



