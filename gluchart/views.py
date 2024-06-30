from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


def base_view(request: HttpRequest):
    return redirect(reverse("values:graph"))