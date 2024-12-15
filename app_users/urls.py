from django.urls import path
from rest_framework.routers import DefaultRouter

from app_users import views as user_views

urlpatterns = [
    # auth urls
    path('auth/login/', user_views.LoginView.as_view(), name='login'),
    path('auth/login-with-username/', user_views.LoginWithUsernameView.as_view(), name='login_with_username'),
    path('auth/logout/', user_views.LogoutView.as_view(), name='logout'),
]
