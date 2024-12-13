from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from app_common.premissions import IsOwnerOrReadOnly
from .serializers import BasketSerializer
from .models import BasketModel


class BasketView(View):
    serializer_class = BasketSerializer
    queryset = BasketModel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)