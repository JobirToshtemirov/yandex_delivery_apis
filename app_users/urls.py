from django.urls import path
from rest_framework.routers import DefaultRouter

from app_users import views as user_views

urlpatterns = [
    # auth urls
    path('auth/login/', user_views.LoginView.as_view(), name='login'),
    path('auth/logout/', user_views.LogoutView.as_view(), name='logout'),
]
