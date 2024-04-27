from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('values', views.GlucoseValueViewSet, 'values-api')

app_name = 'values-api'
urlpatterns = router.urls

urlpatterns += [path('values/batch', views.GlucoseValueBatchCreate.as_view())]
