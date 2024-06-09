import json
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
    

def graph_component(request):
    template_name = 'graph_component.html'
    max_readings = 400
    n_readings = min(max_readings, GlucoseValue.objects.filter(user=request.user.id).count())
    values = GlucoseValue.objects.filter(user=request.user.id).order_by("-time_of_reading")[:n_readings]
    timestamps = [value.time_of_reading.isoformat() for value in values]
    readings = [float(v.value) if v.value else None for v in values]



    return render(request, template_name, {
        "x_values": f"{timestamps}",
        "y_values": f"{readings}".replace("None", "").replace("\'", "").replace("\"", ""),
        "x_range_min": (values[0].time_of_reading - timedelta(hours=2)).isoformat(), 
        "x_range_max": values[0].time_of_reading.isoformat(),        
    })


def htmx_component(request):
    template_name = 'htmx_component.html'
    return render(request, template_name)


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


def htmx_base(request):
    template_name = 'htmx_base.html'
    return render(request, template_name)


class EntriesView(views.View):
    def get(self, request):
        return HttpResponse(GlucoseValue.objects.filter(time_of_reading__lt="2020-01-06T00:00:00Z").values('time_of_reading', 'value'))
    






    

