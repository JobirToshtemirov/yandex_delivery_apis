from django.contrib import admin

from app_basket.models import BasketItemModel, BasketModel


admin.site.register(BasketItemModel)
admin.site.register(BasketModel)