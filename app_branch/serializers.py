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
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of product IDs to add or remove."
    )
    action = serializers.ChoiceField(
        choices=ActionChoice.choices,
        default=ActionChoice.ADD,
        help_text="Action to perform: 'add' or 'remove'."
    )