from django.urls import path, include

from . import views


app_name = "sources"
url_patterns = [
    path('source', views.SourceView.as_view(), name='source'),
    path('source/new', views.SourceAddView.as_view(), name='new_source'),
    path('source/new/2', views.add_new_source, name='new_source_2'),
    path('llu', views.get_llu_data, name='llu_data')
]