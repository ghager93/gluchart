from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import views

from sources.utils import llu_datetime
from values.models import GlucoseValue
from . import librelinkup
from .models import Source
from .forms import LibreLinkUp
    

class SourceView(views.View):
    template_name = 'data_sources.html'
    def get(self, request):
        sources = Source.objects.filter(user=request.user).order_by("created_at")

        return render(request, self.template_name, {
            "sources": sources
        })


class SourceAddView(views.View):
    template_name = 'add_data_source.html'
    def get(self, request):
        form = LibreLinkUp()
        return render(request, self.template_name, {
            "form": form
        })
    
    def post(self, request):
        form = LibreLinkUp(request.POST)
        if form.is_valid():
            token, token_expiry = librelinkup.get_token(form.cleaned_data["email"], form.cleaned_data["password"])
            patient_id = librelinkup.get_patient_id(token)
            sensor_start, graph_data = librelinkup.get_device_info(token, patient_id)

            cache_data = {
                "name": form.cleaned_data["name"],
                "token": token,
                "token_expiry": token_expiry,
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
                "patient_id": patient_id,
                "sensor_start": sensor_start,
                "graph_data": graph_data,
            }

            cache_key = f"new_source_{request.session.session_key}"
            cache.set(cache_key, cache_data, timeout=3600)
            
            return render(request, "data_source_found.html")
        

def add_new_source(request):
    cache_key = f"new_source_{request.session.session_key}"
    data = cache.get(cache_key)

    new_source = Source(
        name=data["name"],
        type="libre_link_up",
        token=data["token"],
        token_expiry=datetime.fromtimestamp(int(data["token_expiry"])),
        email=data["email"],
        password=data["password"],
        patient_id=data["patient_id"],
        sensor_start=datetime.fromtimestamp(int(data["sensor_start"])),
        user=User.objects.get(id=request.user.id)
    )
    new_source.save()

    values = []
    for entry in data["graph_data"]:
        entry["user"] = request.user
        entry["source"] = new_source
        entry["time_of_reading"] = llu_datetime(entry["timestamp"])
        value = GlucoseValue(**entry)
        value.save()
        values.append(value)

    return redirect("graph")


def get_llu_data(request):
    for source in Source.objects.filter(user=request.user, type="libre_link_up"):
        try:
            _, graph_data = librelinkup.get_device_info(source.token, source.patient_id)
        
            values = []
            for entry in graph_data:
                entry["user"] = request.user
                entry["source"] = source
                entry["time_of_reading"] = llu_datetime(entry["timestamp"])
                value = GlucoseValue(**entry)
                value.save()
                values.append(value)
        except:
            pass
        
    return redirect("graph")


    
class EntriesView(views.View):
    def get(self, request):
        return HttpResponse(GlucoseValue.objects.filter(time_of_reading__lt="2020-01-06T00:00:00Z").values('time_of_reading', 'value'))
    






    

