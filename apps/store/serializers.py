from rest_framework.serializers import Serializer,ModelSerializer
# Internal
from .models import Shop,Category,Product,ProductImage,ProductVariant

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
