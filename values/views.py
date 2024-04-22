import math
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import views

from .models import GlucoseValue


class GraphView(views.View):
    template_name = 'graph.html'
    max_readings = 400

    def get(self, request):
        n_readings = min(self.max_readings, GlucoseValue.objects.filter(user=request.user.id).count())
        values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:n_readings]
        timestamps = [value.time_of_reading.isoformat() for value in values]
        readings = [float(v.value) if v.value else None for v in values]
        if values[0] and values[1]:
            arrow_angle = -int(math.degrees(math.atan(float(values[0].value) - float(values[1].value))))
        else:
            arrow_angle = 0
        return render(request, self.template_name, {
            "x_values": f"{timestamps}",
            "y_values": f"{readings}".replace("None", "").replace("\'", "").replace("\"", ""),
            "x_range_min": (values[0].time_of_reading - timedelta(hours=2)).isoformat(), 
            "x_range_max": values[0].time_of_reading.isoformat(),
            "last_reading": values[0].value,
            "arrow_angle": arrow_angle,
        })
    

class EntriesView(views.View):
    def get(self, request):
        return HttpResponse(GlucoseValue.objects.filter(time_of_reading__lt="2020-01-06T00:00:00Z").values('time_of_reading', 'value'))
    






    

