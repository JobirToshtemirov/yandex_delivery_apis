from rest_framework import serializers

from app_branch.models import ActionChoice


class AcceptSerializers(serializers.Serializer):
    """
    Serializer for accepting an order.
    """
    order_id = serializers.IntegerField()


class AddOrRemoveProductsSerializer(serializers.Serializer):
    """
    Serializer for adding or removing products from an order.
    """
    product_ids = serializers.ManyRelatedField()
    action = serializers.CharField(max_length=8, choices=ActionChoice, default=ActionChoice.ADD)
