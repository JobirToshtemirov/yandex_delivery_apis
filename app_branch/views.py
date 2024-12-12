from rest_framework import generics, status
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


class AddOrRemove(APIView):
    """
    Add or remove orders from the client.
    """
    permission_classes = [IsAuthenticated, IsBranch]
    queryset = BranchProductsModel
    serializer_class = AddOrRemoveProductsSerializer

    def post(self, request):
        """
        Add or remove the order.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            for item in serializer.validated_data.get('product_ids'):
                order = self.queryset.objects.filter(restaurant__product_id=item)
                if order.exists():
                    order = order.delete()
                    if item['action'] == ActionChoice.ADD:
                        order.items.add(item['product_id'])
                    else:
                        order.items.remove(item['product_id'])
                    order.save()





