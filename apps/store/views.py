from django.shortcuts import render,get_object_or_404
# Internal
from .models import Shop,Category,Product,ProductImage,ProductVariant
from .serializers import ShopOwnerSerializer,ShopCustomerSerializer
from .permissions import CustomShopPermission
# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status

class ShopView(APIView):  
    permission_classes = [CustomShopPermission] 

    def get(self,request):
        # Public Data
        queryset = Shop.objects.filter(is_active=True)
        serializer = ShopCustomerSerializer(queryset,many=True)

        # IF use Header
        user = request.user
        if user.is_authenticated:
            queryset = Shop.objects.filter(owner=user)
            serializer = ShopOwnerSerializer(queryset,many=True)

        return Response(serializer.data, status=200)

    def post(self,request):
        user = request.user

        if Shop.objects.filter(owner=user).exists():
            return Response({'detail':"Already you have an store!"},status=status.HTTP_409_CONFLICT)

        serializer = ShopOwnerSerializer(data=serializer.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user) 
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def put(self, request):
        return self.update(request, partial=False) 
    def patch(self, request):
        return self.update(request, partial=True) 
    
    def update(self, request, partial):
        user = request.user
        shop = Shop.objects.filter(owner=user).first() 
        if not shop:
            return Response({"detail":"No shop found!"},status=status.HTTP_404_NOT_FOUND)
        if not shop.is_verified:
            return Response({'detail':"Your shop verification is still processing. After verification, you can update data!"},status=status.HTTP_403_FORBIDDEN)

        serializer = ShopOwnerSerializer(shop,data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

