"""
URL configuration for gluchart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views



# router = routers.DefaultRouter()
# router.register('api/users', include('users.api.urls'))
# router.register('api/sources', include('sources.api.urls'))
# router.register('api/values', include('values.api.urls'))

# urlpatterns = [
#     path('', include(router.urls)),
#     path('admin/', admin.site.urls),
#     path('batch', views.GlucoseValueBatchCreate.as_view(), name='batch'),
#     path('graph', views.GraphView.as_view(), name='graph'),
#     path('data_sources', views.DataSourceView.as_view(), name='data_sources'),
#     path('data_sources/add', views.AddDataSourceView.as_view(), name='add_data_source'),
#     path('data_sources/add/2', views.add_new_source, name='add_data_source2'),
#     path('llu_data', views.get_llu_data, name='llu_data'),
#     path('entries', views.EntriesView.as_view(), name='entries')
# ]

urlpatterns = [
    path('', views.base_view, name="base_view"),
    
    path('api/', include('users.api.urls')),
    path('api/', include('sources.api.urls')),
    path('api/', include('values.api.urls')),

    path('', include('sources.urls')),
    path('', include('values.urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
