from rest_framework.serializers import Serializer,ModelSerializer,SlugRelatedField
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

# ---------------------------
# Category Serializer
# ---------------------------
class CategorySerializer(ModelSerializer):
    shop = SlugRelatedField(slug_field='slug',queryset=Shop.objects.all())
    parent = SlugRelatedField(slug_field='slug',queryset=Category.objects.all())

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
        
# ---------------------------
# Product Serializer
# ---------------------------
class ProductSerializer(ModelSerializer):
    shop = SlugRelatedField(slug_field='slug',queryset=Shop.objects.all())
    category = SlugRelatedField(slug_field='slug',queryset=Category.objects.all())

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
    product = SlugRelatedField(slug_field='slug',queryset=Product.objects.all())

    class Meta:
        model = ProductImage
        fields = "__all__" 

    def validate_product(self,value):
        user = self.context['request'].user
        if value is None:
            return value
        
        if value.shop.owner != user:
            raise ValidationError("Product must belong to your shop! Not Found Product!")


# ---------------------------
# Product Image Serializer
# ---------------------------
class ProductVariantSerializer(ModelSerializer):
    product = SlugRelatedField(slug_field='slug',queryset=Product.objects.all())

    class Meta:
        model = ProductVariant
        fields = "__all__" 

    def validate_product(self,value):
        user = self.context['request'].user
        if value is None:
            return value
        
        if value.shop.owner != user:
            raise ValidationError("Product must belong to your shop! Not Found Product!")
