from django.urls import path, include

from . import views


app_name = "values"
urlpatterns = [
    path('graph/', views.graph_view, name='graph'),
    path('htmx-graph/', views.htmx_graph, name='htmx_graph'),
    path('htmx-arrow/', views.htmx_arrow, name='htmx_arrow')
]