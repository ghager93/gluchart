from django.db import models
from django.contrib.auth.models import User

from sources.models import Source


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



