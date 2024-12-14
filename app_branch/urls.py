from django.urls import path

from app_branch import views


app_name = 'app_branch'

urlpatterns = [
    path('pending-for-restaurant-orders/', views.PendingForRestaurantOrders.as_view(), name='pending_for_restaurant_orders'),
    path('accept-orders/', views.AcceptOrders.as_view(), name='accept_orders'),
    path('add-or-remove/', views.AddOrRemoveBranchProducts.as_view(), name='add_or_remove'),
    path('branch-statistics/', views.BranchStatistics.as_view(), name='branch-statistics'),
]