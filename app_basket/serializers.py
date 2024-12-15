from .models import BasketModel, BasketItemModel
from rest_framework import serializers


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItemModel
        fields = '__all__'

    def validate(self, data):
        if data['quantity'] < 1:
            raise serializers.ValidationError("Quantity should be greater than 0")
        elif data['price'] < 0:
            raise serializers.ValidationError("Price should be greater than or equal to 0")
        elif data['total_price'] < 0:
            raise serializers.ValidationError("Total price should be greater than or equal to 0")
        elif data['total_price'] > data['price'] * data['quantity']:
            raise serializers.ValidationError("Total price should be less than or equal to price * quantity")
        elif data['user'] is None:
            raise serializers.ValidationError("User should be provided")
        elif data['user'] == self.context['request'].user:
            raise serializers.ValidationError("User should not be the same as the current user")
        return data
