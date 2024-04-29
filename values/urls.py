from django.urls import path, include

from . import views


app_name = "values"
urlpatterns = [
    path('graph/', views.GraphView.as_view(), name='graph'),
    path('entries/', views.EntriesView.as_view(), name='entries'),
]