from rest_framework.serializers import Serializer, ModelSerializer, SlugRelatedField
# Internal
from .models import Order, OrderItem
from apps.store.models import Product

# ---------------------------
# Order Item Serializer
# ---------------------------
class OrderItemSerializer(ModelSerializer):
    # Slug Prodcut show
    product = SlugRelatedField(slug_field='slug',queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = "__all__"

# ---------------------------
# Order Serializer
# ---------------------------
class OrderSerializer(ModelSerializer):
    # Nested Data
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

