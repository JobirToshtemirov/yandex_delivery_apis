from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from app_common.premissions import IsOwnerOrReadOnly
from .serializers import BasketSerializer
from .models import BasketModel


class BasketView(View):
    serializer_class = BasketSerializer
    queryset = BasketModel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        basket = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(basket, many=True)
        response = {
            'success': True,
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)
