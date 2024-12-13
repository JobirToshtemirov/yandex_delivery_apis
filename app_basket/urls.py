from django.urls import path
from . import views

app_name = 'app_basket'

urlpatterns = [
    path('', views.BasketView.as_view(), name='basket'),
    path('submit/', views.ChangeBasketStatusView.as_view(), name='basket_submit'),
]
