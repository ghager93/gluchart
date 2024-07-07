import json
import math
from datetime import timedelta

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import views, permissions

from .models import GlucoseValue


@login_required    
def graph_view(request: HttpRequest):
    template_name = "graph.html"

    max_readings = 400
    n_readings = min(max_readings, GlucoseValue.objects.filter(user=request.user.id).count())
    values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:n_readings]
    timestamps = [value.time_of_reading.isoformat() for value in values]
    readings = [float(v.value) if v.value else None for v in values]
    if values[0] and values[1]:
        arrow_angle = -int(math.degrees(math.atan(float(values[0].value) - float(values[1].value))))
    else:
        arrow_angle = 0

    return render(request, template_name, {
        "x_values": f"{timestamps}",
        "y_values": f"{readings}".replace("None", "").replace("\'", "").replace("\"", ""),
        "x_range_min": (values[0].time_of_reading - timedelta(hours=2)).isoformat(), 
        "x_range_max": values[0].time_of_reading.isoformat(),
        "last_reading": values[0].value,
        "arrow_angle": arrow_angle,
    })    


def htmx_graph(request):
    template_name = 'htmx_graph.html'

    max_readings = 400
    n_readings = min(max_readings, GlucoseValue.objects.filter(user=request.user.id).count())
    values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:n_readings]
    timestamps = [value.time_of_reading.isoformat() for value in values]
    readings = [float(v.value) if v.value else None for v in values]

    initial_data = {
        'x': timestamps,
        'y': readings,
        'xMin': (values[0].time_of_reading - timedelta(hours=2)).isoformat(),
        'xMax': values[0].time_of_reading.isoformat(),
        'yRange': [0, 20]
    }
    update_url = "test_url"
    update_interval = 100

    return render(request, template_name, {
        "initial_data": json.dumps(initial_data),
        "update_url": update_url,
        "update_interval": update_interval
    })


def htmx_arrow(request):
    template_name = 'htmx_arrow.html'

    last_values = GlucoseValue.objects.filter(user=request.user.id).order_by('-timestamp')[:2]

    if last_values[0] and last_values[1]:
        arrow_angle = -int(math.degrees(math.atan(float(last_values[0].value) - float(last_values[1].value))))
    else:
        arrow_angle = 0

    return render(request, template_name, {
        "value": last_values[0].value,
        "timestamp": last_values[0].timestamp,
        "arrow_angle": arrow_angle
    })


    

