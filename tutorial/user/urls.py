from rest_framework import routers
from django.urls import path, include
from .views import PersonViewSet

router = routers.DefaultRouter()
router.register("person", PersonViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
