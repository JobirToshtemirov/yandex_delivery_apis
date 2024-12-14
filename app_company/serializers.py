from rest_framework import serializers

from app_branch.models import BranchModel, ActionChoice
from app_company.models import RestaurantProductsModel


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchModel
        fields = '__all__'
        read_only_fields = ('restaurant',)


class CreateRestaurantProductSerializer(serializers.Serializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of product IDs to add or remove."
    )
    action = serializers.ChoiceField(
        choices=ActionChoice.choices,
        default=ActionChoice.ADD,
        help_text="Action to perform: 'add' or 'remove'."
    )
