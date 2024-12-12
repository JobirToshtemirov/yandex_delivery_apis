from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_company.views import BranchViewSet

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
