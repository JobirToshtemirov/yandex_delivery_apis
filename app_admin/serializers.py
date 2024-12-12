from rest_framework import serializers
from app_users.models import UserModel


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
