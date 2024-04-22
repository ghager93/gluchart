from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
