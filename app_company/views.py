from datetime import timedelta

from django.utils import timezone

from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from app_branch.models import BranchModel, ActionChoice
from app_common.premissions import IsRestaurant
from app_company.models import RestaurantModel, RestaurantProductsModel
from app_company.serializers import BranchSerializer, CreateRestaurantProductSerializer
from app_deliveries.models import OrderModel, OrderStatus
from app_users.models import UserRoleChoice


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsRestaurant]

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


class AddOrRemoveRestaurantProducts(generics.CreateAPIView):
    serializer_class = CreateRestaurantProductSerializer
    permission_classes = [IsAuthenticated, IsRestaurant]
    queryset = RestaurantProductsModel.objects.all()

    def perform_create(self, serializer: CreateRestaurantProductSerializer):
        """
        Assign the product to the restaurant managed by the logged-in manager.
        """
        product_ids = serializer.validated_data.get('product_ids')
        action = serializer.validated_data['action']
        restaurant = self.request.user.restaurant  # Assuming the user is linked to a restaurant.
        products = self.queryset.filter(product_id__in=product_ids, restaurant=restaurant)

        if not products.exists():
            return Response(
                data={
                    "success": False,
                    "message": "No matching products found for the restaurant.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Perform action
        if action == ActionChoice.ADD:
            restaurant.products.add(*products)  # Add products
            message = f"Products added successfully."
        elif action == ActionChoice.REMOVE:
            restaurant.products.remove(*products)  # Remove products
            message = f"Products removed successfully."
        else:
            return Response(
                data={"success": False, "message": "Invalid action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={
                "success": True,
                "message": message,
            },
            status=status.HTTP_200_OK,
        )


class RestaurantStatistics(APIView):
    """
    Endpoint to fetch restaurant statistics.
    """
    permission_classes = [IsAuthenticated, IsRestaurant]
    queryset = OrderModel.objects.all()
    fbd_filters = {
        'weekly': timedelta(days=7),
        'monthly': timedelta(days=30),
        'yearly': timedelta(days=365),
    }
    fbt_filters = {
        'delivered': OrderStatus.DELIVERED,
        'canceled': OrderStatus.CANCELED,
    }
    fbm_filters = {
        'price_high_to_low': '-total_price',
        'price_low_to_high': 'total_price',
        'quantity_low_to_high': 'total_items',
        'quantity_high_to_low': '-total_items',
    }

    def get(self, request) -> Response:
        """
        Get restaurant statistics.
        """
        orders = self.queryset.filter(restaurant__user=request.user)
        fbd = request.GET.get('fbd')
        fbt = request.GET.get('fbt')
        fbm = request.GET.get('fbm')

        # Apply date filter
        orders = self.apply_date_filter(orders, fbd)

        # Apply status filter
        if fbt in self.fbt_filters:
            orders = orders.filter(order_status=self.fbt_filters[fbt])

        # Apply sorting filter
        if fbm in self.fbm_filters:
            orders = orders.order_by(self.fbm_filters[fbm])

        # Paginate the orders
        paginator = PageNumberPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)

        # Aggregate statistics
        stats = {
            "delivered": orders.filter(order_status=OrderStatus.DELIVERED).count(),
            "canceled": orders.filter(order_status=OrderStatus.CANCELED).count(),
            "total_orders": orders.count(),
        }

        # Return paginated response
        return paginator.get_paginated_response({
            "success": True,
            "data": paginated_orders,
            **stats,
        })

    def apply_date_filter(self, orders, fbd: str):
        """Apply the date filter to the orders queryset."""
        if fbd == 'today':
            start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return orders.filter(created_at__gte=start_of_today)

        elif fbd in self.fbd_filters:
            return orders.filter(created_at__gte=timezone.now() - self.fbd_filters[fbd])
        return orders