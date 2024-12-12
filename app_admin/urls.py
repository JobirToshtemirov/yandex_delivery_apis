from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSet, CourierViewSet

router = DefaultRouter()
router.register('managers', ManagerViewSet)
router.register('couriers', CourierViewSet, basename="co")

urlpatterns = [
    path('', include(router.urls)),
]
