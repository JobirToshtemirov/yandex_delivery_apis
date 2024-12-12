from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from app_branch.models import BranchModel
from app_common.premissions import IsRestaurant
from app_company.models import RestaurantModel
from app_company.serializers import BranchSerializer
from app_users.models import UserRoleChoice


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsRestaurant]

    def get_queryset(self):
        """
        Restrict queryset to branches owned by the restaurant manager.
        """
        user = self.request.user
        if not user.is_authenticated or user.role != UserRoleChoice.RESTAURANT:
            raise PermissionDenied("You do not have access to these resources.")

        return BranchModel.objects.filter(restaurant__manager=user)

    def perform_create(self, serializer):
        """
        Assign the branch to the restaurant managed by the logged-in manager.
        """
        user = self.request.user
        if not user.is_authenticated or user.role != UserRoleChoice.RESTAURANT:
            raise PermissionDenied("You do not have access to create this resource.")

        restaurant = RestaurantModel.objects.filter(manager=user).first()
        if not restaurant:
            raise PermissionDenied("You are not managing any restaurant.")

        serializer.save(restaurant=restaurant)

    @action(detail=False, methods=['get'])
    def my_branches(self, request):
        """
        Custom endpoint to fetch branches owned by the manager.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
