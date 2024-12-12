from rest_framework import serializers

from app_branch.models import BranchModel


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchModel
        fields = '__all__'
        read_only_fields = ('restaurant',)
