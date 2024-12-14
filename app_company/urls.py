from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_company import views

app_name = 'restaurant'

router = DefaultRouter()
router.register('branches', views.BranchViewSet, basename='branch')

urlpatterns = [
    path('branch/', include(router.urls)),
    path('add-or-remove/', views.AddOrRemoveRestaurantProducts.as_view(), name='add_or_remove'),
    path('restaurant-statistics/', views.RestaurantStatistics.as_view(), name='restaurant-statistics'),
]
