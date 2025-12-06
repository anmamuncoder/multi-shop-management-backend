from rest_framework.serializers import Serializer,ModelSerializer
# Internal
from .models import Shop,Category,Product,ProductImage,ProductVariant
from rest_framework.exceptions import ValidationError

class ShopOwnerSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
        # exclude = ('owner','slug')
        read_only_fields = ('owner','slug','is_verified') 

class ShopCustomerSerializer(ModelSerializer):
    class Meta:
        model = Shop
        # fields = "__all__"

        exclude = ('owner','is_verified','total_sales','is_active')

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('shop','slug')

    def validate_parent(self,value):
        user = self.context['request'].user
        if value is None:
            return value
        
        if value.shop.owner != user:
            raise ValidationError("Parent category must belong to your shop! Not Found Parent Category!")

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ('shop','slug')

    def validate_category(self,value):
        user = self.context['request'].user
        if value is None:
            return value
        
        if value.shop.owner != user:
            raise ValidationError("Parent category must belong to your shop! Not Found Parent Category!")

# ---------------------------
# Product Image Serializer
# ---------------------------
class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__" 

    def validate_product(self,value):
        user = self.context['request'].user
        if value is None:
            return value
        
        if value.shop.owner != user:
            raise ValidationError("Product must belong to your shop! Not Found Product!")
