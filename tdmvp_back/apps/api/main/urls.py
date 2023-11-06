from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MainViewSet


router = DefaultRouter()
router.register('', MainViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
