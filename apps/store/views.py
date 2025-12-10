from django.shortcuts import render,get_object_or_404
# Internal
from .models import Shop,Category,Product,ProductImage,ProductVariant
from .serializers import ShopOwnerSerializer,ShopCustomerSerializer,CategorySerializer,ProductListSerializer,ProductDetailSerializer,ProductImageSerializer,ProductVariantSerializer
from .permissions import Get_AllowAny_Other_IsAuthenticated 
from .filters import ProductFilter
# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.base.paginations import BasePagination
from django_filters.rest_framework import DjangoFilterBackend

class ShopView(ModelViewSet):
    permission_classes = [Get_AllowAny_Other_IsAuthenticated] 
    serializer_class = ShopCustomerSerializer
    queryset = Shop.objects.none()
    lookup_field = 'slug'

    def get_serializer_class(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return ShopOwnerSerializer
        return ShopCustomerSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'shop_owner':
            # Shop owner sees all if include Header Token
            return Shop.objects.filter(owner=user) 
        # Public users see only active categories
        return Shop.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user 
        if Shop.objects.filter(owner=user).exists():
            raise ValidationError({"detail": "You already own a shop!"})
        
        serializer.save(owner=user)

    def perform_update(self, serializer):
        user = self.request.user
        shop = Shop.objects.filter(owner=user).first()
        if shop and not shop.is_verified:
            raise PermissionDenied("Your shop verification is still processing. After verification, you can update data!")
        
        serializer.save()
 
# ---------------------------
# Category View
# ---------------------------
class CategoryView(ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [Get_AllowAny_Other_IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'shop'):
                # Shop owner sees all if include Header Token
                return Category.objects.filter(shop=user.shop)
            return Category.objects.none()
        
        # Public users see only active categories
        return Category.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        user = self.request.user   
        shop = Shop.objects.filter(owner=user).first()
        if not shop:
            raise PermissionDenied("You have no shop available!")
        serializer.save(shop=shop)

# ---------------------------
# Product View
# ---------------------------

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [Get_AllowAny_Other_IsAuthenticated]
    pagination_class = BasePagination
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_class = ProductFilter  
    
    search_fields = ['name', 'slug','tags'] # SEARCHABLE: like search box (?search=three) 
    # filterset_fields = ['category','is_available'] # FILTER:  exict match (?search=three) 
    ordering_fields = ['price','name', 'created_at'] # ORDERING: (?ordering=name or ?ordering=-created_at)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'shop'):
                # Shop owner sees all if include Header Token
                return Product.objects.filter(shop=user.shop)
            return Product.objects.none()
        
        # Public users see only active categories
        return Product.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user   
        shop = Shop.objects.filter(owner=user).first()
        if not shop:
            raise PermissionDenied("You have no shop available!")
        serializer.save(shop=shop)

# ---------------------------
# Product Image View
# ---------------------------
class ProductImageView(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [Get_AllowAny_Other_IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'shop'):
                # Shop owner sees all if include Header Token
                return ProductImage.objects.filter(product__shop=user.shop)
            return ProductImage.objects.none()
        
        # Public users see only active categories
        return ProductImage.objects.all()
    
# ---------------------------
# Product Variant View
# ---------------------------
class ProductVariantView(ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [Get_AllowAny_Other_IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'shop'):
                # Shop owner sees all if include Header Token
                return ProductVariant.objects.filter(product__shop=user.shop)
            return ProductVariant.objects.none()
        
        # Public users see only active categories
        return ProductVariant.objects.all()
