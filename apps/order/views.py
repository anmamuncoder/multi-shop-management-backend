from django.shortcuts import render

# Create your views here.
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from .permissions import GETOwnerAllCustomer

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class OrderView(ModelViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer 
    permission_classes = [GETOwnerAllCustomer]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.role == "customer":
                return Order.objects.filter(customer=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(customer=user)
        serializer.save()   


class OrderItemView(ModelViewSet):
    queryset = OrderItem.objects.none()
    serializer_class = OrderItemSerializer
    permission_classes = [GETOwnerAllCustomer]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.role == "customer":
                return OrderItem.objects.filter(order__customer=user)
            if user.role == "shop_owner":
                return OrderItem.objects.filter(product__shop=user.shop)

        return OrderItem.objects.none()
    