from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('sources', views.SourceViewSet)

app_name = 'sources-api'
urlpatterns = router.urls
