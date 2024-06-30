from django.urls import path, include

from . import views


app_name = "values"
urlpatterns = [
    path('graph/', views.graph_view, name='graph'),
    path('entries/', views.EntriesView.as_view(), name='entries'),
    path('htmx-component/', views.htmx_component, name='htmx_component'),
    path('htmx-graph/', views.htmx_graph, name='htmx_graph'),
    path('htmx-base/', views.htmx_base, name='htmx_base')
]