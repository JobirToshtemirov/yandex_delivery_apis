from datetime import timedelta

from django.utils import timezone

from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_branch.models import BranchProductsModel, ActionChoice
from app_branch.serializers import AcceptSerializers, AddOrRemoveProductsSerializer
from app_common.premissions import IsBranch
from app_deliveries.models import OrderModel, OrderStatus
from app_deliveries.serializers import OrderSerializer


class PendingForRestaurantOrders(generics.ListAPIView):
    """
    Returns a list of pending orders for restaurant.
    """
    permission_classes = [IsAuthenticated, IsBranch]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderModel.objects.filter(order_status=OrderStatus.PENDING_RESTAURANT)


class AcceptOrders(APIView):
    """
    Accepts new orders from the client.
    """
    permission_classes = [IsAuthenticated, IsBranch]
    queryset = OrderModel

    def post(self, request):
        """
        Accept the order.
        """
        serializer = AcceptSerializers(data=request.data)
        if serializer.is_valid():
            order = self.queryset.objects.filter(id=serializer.validated_data.get('order_id'))
            if order.exists():
                order = order.first()
                order.order_status = OrderStatus.CONFIRMED_RESTAURANT
                order.save()
                data = OrderSerializer(order).data
                return Response(data={
                    "success": True,
                    "message": "Order accepted",
                    "data": data
                }, status=status.HTTP_201_CREATED)
        return Response(data={
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AddOrRemoveBranchProducts(APIView):
    """
    Add or remove products from the branch's order list.
    """
    permission_classes = [IsAuthenticated, IsBranch]
    queryset = BranchProductsModel.objects.all()
    serializer_class = AddOrRemoveProductsSerializer

    def post(self, request):
        """
        Add or remove products to/from the branch's orders.
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "success": False,
                    "message": "Invalid data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_ids = serializer.validated_data['product_ids']
        action = serializer.validated_data['action']
        branch = request.user.branch  # Assuming the user is linked to a branch.
        products = self.queryset.filter(restaurant__product_id__in=product_ids, branch=branch)

        if not products.exists():
            return Response(
                data={
                    "success": False,
                    "message": "No matching products found for the branch.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Perform action
        if action == ActionChoice.ADD:
            branch.products.add(*products)  # Add products
            message = f"Products added successfully."
        elif action == ActionChoice.REMOVE:
            branch.products.remove(*products)  # Remove products
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


class BranchStatistics(APIView):
    """
    API view to return statistics and order data for a branch.

    This view allows authenticated branch users to fetch statistics and order details
    based on various filters and sorting criteria. The response is paginated for ease of use.

    ### Permissions
    - The user must be authenticated.
    - The user must have branch-level access (checked via the `IsBranch` permission).

    ### Available Filters
    - **Date Filter (`fbd`)**:
        - `today`: Orders created today.
        - `weekly`: Orders from the past 7 days.
        - `monthly`: Orders from the past 30 days.
        - `yearly`: Orders from the past 365 days.
    - **Status Filter (`fbt`)**:
        - `delivered`: Orders with a status of delivered.
        - `confirmed`: Orders confirmed by the restaurant.
        - `pending`: Orders pending acceptance by the restaurant.
        - `canceled`: Canceled orders.
    - **Sorting Filter (`fbm`)**:
        - `price_high_to_low`: Orders sorted by total price in descending order.
        - `price_low_to_high`: Orders sorted by total price in ascending order.
        - `quantity_low_to_high`: Orders sorted by total items in ascending order.
        - `quantity_high_to_low`: Orders sorted by total items in descending order.

    ### Response
    - Paginated order data.
    - Aggregated statistics:
        - `delivered`: Count of delivered orders.
        - `confirmed_orders`: Count of confirmed orders.
        - `pending_to_accept`: Count of pending orders.
        - `canceled`: Count of canceled orders.
        - `total_orders`: Total number of orders in the result set.

    ### Query Parameters
    - `fbd` (optional): Date filter. One of `today`, `weekly`, `monthly`, or `yearly`.
    - `fbt` (optional): Status filter. One of `delivered`, `confirmed`, `pending`, or `canceled`.
    - `fbm` (optional): Sorting filter. One of `price_high_to_low`, `price_low_to_high`,
      `quantity_low_to_high`, or `quantity_high_to_low`.

    ### Example Request
    ```
    GET /api/branch-statistics/?fbd=weekly&fbt=delivered&fbm=price_high_to_low
    ```

    ### Example Response
    ```json
    {
        "count": 10,
        "next": "http://example.com/api/branch-statistics/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "branch": "Branch A",
                "order_status": "delivered",
                "total_price": 150.0,
                "total_items": 3,
                "created_at": "2024-12-01T12:00:00Z"
            },
        ]
        "delivered": 5,
        "confirmed_orders": 3,
        "pending_to_accept": 2,
        "canceled": 1,
        "total_orders": 10
    }
    ```
    """
    permission_classes = [IsAuthenticated, IsBranch]
    queryset = OrderModel.objects.all()
    fbd_filters = {
        'weekly': timedelta(days=7),
        'monthly': timedelta(days=30),
        'yearly': timedelta(days=365),
    }
    fbt_filters = {
        'delivered': OrderStatus.DELIVERED,
        'confirmed': OrderStatus.CONFIRMED_RESTAURANT,
        'pending': OrderStatus.PENDING_RESTAURANT,
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
        Get branch statistics.
        """
        orders = self.queryset.filter(branch__user=request.user)
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
            "confirmed_orders": orders.filter(order_status=OrderStatus.CONFIRMED_RESTAURANT).count(),
            "pending_to_accept": orders.filter(order_status=OrderStatus.PENDING_RESTAURANT).count(),
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