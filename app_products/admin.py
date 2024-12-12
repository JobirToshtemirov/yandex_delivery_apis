from django.contrib import admin

from app_products.models import ProductImageModel, ProductsModel, CategoryModel

admin.site.register(CategoryModel)
admin.site.register(ProductImageModel)
admin.site.register(ProductsModel)