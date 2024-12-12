from .models import BasketModel
from rest_framework import serializers


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketModel
        fields = '__all__'
