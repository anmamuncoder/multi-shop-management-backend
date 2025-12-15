from django.shortcuts import render

# Create your views here.
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from .permissions import GETOwnerAllCustomer
from apps.base.permissions import IsCustomer, IsShopOwner

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

class OrderView(ModelViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated,IsCustomer]

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
    filter_backends = [DjangoFilterBackend]
    filter_classes = ['product','status']

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.role == "customer":
                return OrderItem.objects.filter(order__customer=user)
            if user.role == "shop_owner":
                return OrderItem.objects.filter(product__shop=user.shop)

        return OrderItem.objects.none()
    

    def check_order(self, serializer_or_instance):
        """
        If order is not pending that time cant add any items or edit or delete
        """
        if hasattr(serializer_or_instance, 'instance') and serializer_or_instance.instance:
            order = serializer_or_instance.instance.order
        else:
            order = serializer_or_instance.validated_data['order']
        if order.status != 'pending':
            raise PermissionDenied("Cannot create, update, or delete item for order which is not pending.")

    def perform_create(self, serializer):
        self.check_order(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        self.check_order(serializer)
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        self.check_order(instance) 
        return super().perform_destroy(instance)
