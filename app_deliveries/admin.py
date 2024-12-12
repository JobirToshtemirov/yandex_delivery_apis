from django.contrib import admin

from app_deliveries.models import OrderItemModel, OrderModel

admin.site.register(OrderItemModel)
admin.site.register(OrderModel)