from django.contrib import admin

from app_users.models import UserLocations, UserModel

admin.site.register(UserLocations)
admin.site.register(UserModel)