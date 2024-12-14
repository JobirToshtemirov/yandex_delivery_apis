from datetime import timedelta

from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_common.premissions import IsCourier
from app_deliveries.models import OrderModel, OrderStatus
from app_deliveries.serializers import OrderSerializer


class MyDeliveredDeliveries(generics.ListAPIView):
    """
    Retrieve a list of delivered deliveries for a specific user.
    """
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCourier]

    def get_queryset(self):
        """
        Return delivered deliveries for the authenticated courier.
        """
        return self.queryset.filter(courier=self.request.user, order_status=OrderStatus.DELIVERED)


class StatisticsCourier(APIView):
    """
    API view to retrieve delivery statistics for a specific courier.

    This view provides statistics related to the orders assigned to a courier,
    including the total number of assigned, delivered, and canceled orders, as well as
    the total earnings and average price of delivered orders. It also allows filtering
    by specific date ranges.

    ### Permissions
    - The user must be authenticated.
    - The user must have courier-level access (checked via the `IsCourier` permission).

    ### Available Filters
    - **Date Filter (`fbd`)**:
        - `today`: Orders created today.
        - `weekly`: Orders from the past 7 days.
        - `monthly`: Orders from the past 30 days.
        - `yearly`: Orders from the past 365 days.

    ### Response
    - **Order Data**:
        - Paginated list of orders assigned to the courier.
        - Each order contains:
            - `id`: The unique ID of the order.
            - `total_price`: The total price of the order.
            - `order_status`: The current status of the order.
            - `created_at`: The date and time when the order was created.
    - **Statistics**:
        - `total_assigned_orders`: Total number of orders assigned to the courier.
        - `total_delivered_orders`: Total number of delivered orders.
        - `total_canceled_orders`: Total number of canceled orders.
        - `total_sum`: Total earnings from delivered orders.
        - `average_delivered_order_price`: Average price of delivered orders.
        - `pending_order`: The first pending order for the courier, if any.

    ### Query Parameters
    - `fbd` (optional): Date filter. One of `today`, `weekly`, `monthly`, or `yearly`.

    ### Example Request
    ```
    GET /api/courier-statistics/?fbd=weekly
    ```

    ### Example Response
    ```json
    {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "total_price": 120.5,
                "order_status": "delivered",
                "created_at": "2024-12-12T10:00:00Z"
            },
            {
                "id": 2,
                "total_price": 80.0,
                "order_status": "canceled",
                "created_at": "2024-12-11T15:30:00Z"
            }
        ],
        "total_assigned_orders": 10,
        "total_delivered_orders": 6,
        "total_canceled_orders": 2,
        "total_sum": 450.0,
        "average_delivered_order_price": 75.0,
        "pending_order": {
            "id": 3,
            "total_price": 50.0,
            "order_status": "pending",
            "created_at": "2024-12-13T09:00:00Z"
        }
    }
    ```
    """
    permission_classes = [IsAuthenticated, IsCourier]
    queryset = OrderModel.objects.all()
    fbd_filters = {
        'weekly': timedelta(days=7),
        'monthly': timedelta(days=30),
        'yearly': timedelta(days=365),
    }

    def get(self, request):
        """
        Get delivery statistics for the courier.
        """
        courier = self.request.user
        orders = self.queryset.filter(courier=courier)

        fbd = request.GET.get('fbd')

        # Apply date filter
        orders = self.apply_date_filter(orders, fbd)

        # Calculate statistics manually
        delivered_orders = orders.filter(order_status=OrderStatus.DELIVERED)
        delivered_orders_count = delivered_orders.count()

        # Calculate total price manually
        delivered_orders_total_price = sum(
            order.total_price for order in delivered_orders
        )

        total_assigned_orders = orders.count()
        total_canceled_orders = orders.filter(order_status=OrderStatus.CANCELED).count()

        # Calculate average price of delivered orders (avoid division by zero)
        average_delivered_order_price = (
            delivered_orders_total_price / delivered_orders_count
            if delivered_orders_count > 0 else 0
        )

        # Prepare response data
        data = {
            "data": orders,
            "total_assigned_orders": total_assigned_orders,
            "total_delivered_orders": delivered_orders_count,
            "total_canceled_orders": total_canceled_orders,
            "total_sum": delivered_orders_total_price,
            "average_delivered_order_price": round(average_delivered_order_price, 2),
            "pending_order": orders.filter(order_status=OrderStatus.PENDING_COURIER).first()
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def apply_date_filter(self, orders, fbd: str):
        """Apply the date filter to the orders queryset."""
        if fbd == 'today':
            start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return orders.filter(created_at__gte=start_of_today)

        elif fbd in self.fbd_filters:
            return orders.filter(created_at__gte=timezone.now() - self.fbd_filters[fbd])
        return orders


class AcceptForDelivering(APIView):
    """
    Accept an order for delivery.
    """
    permission_classes = [IsAuthenticated, IsCourier]
    queryset = OrderModel

    def post(self, request):
        """
        Accept the order for delivery.
        """
        order = self.queryset.objects.filter(
            courier__id=request.user.pk).filter(order_status=OrderStatus.PENDING_COURIER)
        if order.exists():
            order = order.first()
            order.order_status = OrderStatus.PENDING_RESTAURANT
            order.save()
            data = OrderSerializer(order).data
            return Response(data={
                "success": True,
                "message": "Order accepted for delivery",
                "data": data
            }, status=status.HTTP_200_OK)

        return Response(data={
            "success": False,
            "message": "No pending orders found for this courier"
        }, status=status.HTTP_400_BAD_REQUEST)


class MarkAsDelivering(APIView):
    """
    Accept an order for delivery.
    """
    permission_classes = [IsAuthenticated, IsCourier]
    queryset = OrderModel

    def post(self, request):
        """
        Accept the order for delivery.
        """
        order = self.queryset.objects.filter(
            courier__id=request.user.pk).filter(order_status=OrderStatus.CONFIRMED_RESTAURANT)
        if order.exists():
            order = order.first()
            order.order_status = OrderStatus.DELIVERING
            order.save()
            data = OrderSerializer(order).data
            return Response(data={
                "success": True,
                "message": "Order marked as delivering",
                "data": data
            }, status=status.HTTP_200_OK)

        return Response(data={
            "success": False,
            "message": "No confirmed from restaurant orders found"
        }, status=status.HTTP_400_BAD_REQUEST)


class MarkAsDelivered(APIView):
    """
    Mark an order as delivered.
    """
    permission_classes = [IsAuthenticated, IsCourier]
    queryset = OrderModel


    def post(self, request):
        """
        Mark the order as delivered.
        """
        order = self.queryset.objects.filter(
            courier__id=request.user.pk).filter(order_status=OrderStatus.DELIVERING)
        if order.exists():
            order = order.first()
            order.order_status = OrderStatus.DELIVERED
            order.save()
            data = OrderSerializer(order).data
            return Response(data={
                "success": True,
                "message": "Order marked as delivered",
                "data": data
            }, status=status.HTTP_200_OK)

        return Response(data={
            "success": False,
            "message": "No pending delivery order found for this courier"
        }, status=status.HTTP_400_BAD_REQUEST)