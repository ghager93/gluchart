from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)

app_name = 'users-api'
urlpatterns = router.urls
