from django.urls import path
from rest_framework.routers import DefaultRouter

from app_users import views as user_views

router = DefaultRouter()

router.register('users', user_views.UserListView, basename='user')

urlpatterns = [
                  # auth urls
                  path('auth/login/', user_views.LoginView.as_view(), name='login'),
                  path('auth/logout/', user_views.LogoutView.as_view(), name='logout'),
                  path('products/', user_views.GetAllProductsView.as_view(), name='products'),
                  path('user/me/', user_views.GetActiveUserView.as_view(), name='user-me'),
                  path('user/update/', user_views.UpdateProfileView.as_view(), name='update-profile'),
                  path('user/update/password/', user_views.ChangePasswordView.as_view(), name='change-password'),
              ] + router.urls
