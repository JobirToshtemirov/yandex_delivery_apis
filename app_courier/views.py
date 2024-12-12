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
        return self.queryset.filter(courier=self.request.user)


class StatisticsCourier(APIView):
    """
    Retrieve delivery statistics for a specific courier.
    """
    permission_classes = [IsAuthenticated, IsCourier]
    queryset = OrderModel.objects.all()

    def get(self, request):
        """
        Get delivery statistics for the courier.
        """
        courier = self.request.user
        orders = self.queryset.filter(courier=courier)

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
            "total_assigned_orders": total_assigned_orders,
            "total_delivered_orders": delivered_orders_count,
            "total_canceled_orders": total_canceled_orders,
            "total_sum": delivered_orders_total_price,
            "average_delivered_order_price": round(average_delivered_order_price, 2),
            "pending_order": orders.filter(order_status=OrderStatus.PENDING_COURIER).first()
        }

        return Response(data=data, status=status.HTTP_200_OK)



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