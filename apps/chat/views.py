from django.shortcuts import render
from rest_framework import generics 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
# Inner
from .serializers import ChannelSerializer, MessageSerializer
from .models import Channel, Message
from .filters import ChannelFilter
# Enternal
from apps.base.paginations import BasePagination 

# Create your views here.
class ChannelView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChannelFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Channel.objects.filter(customer=user)
        elif user.role == 'shop_owner':
            return Channel.objects.filter(shop__owner=user)
        return Channel.objects.none()
  
# Message with channel id
class MessageView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated] 
    pagination_class = BasePagination
    pagination_class.max_page_size = 100

    def get_queryset(self):
        channel_id = self.kwargs.get("channel_id")
        user = self.request.user

        if not channel_id:
            return Message.objects.none()
        
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
           return Message.objects.none()

        # Permission check 
        if (user.role == "customer" and channel.customer != user) or (user.role == "shop_owner" and channel.shop != user):
            return Message.objects.none()

        return Message.objects.filter(channel=channel) 
