from rest_framework.viewsets import ModelViewSet
from app_users.models import UserModel
from .serializers import ManagerSerializer, CourierSerializer
from rest_framework.permissions import IsAdminUser


class ManagerViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAdminUser]


class CourierViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsAdminUser]
