from rest_framework.serializers import Serializer, ModelSerializer, SlugRelatedField
# Internal
from .models import Order, OrderItem
from apps.store.models import Product
from rest_framework.exceptions import ValidationError

# ---------------------------
# Order Item Serializer
# ---------------------------
class OrderItemSerializer(ModelSerializer):
    # Slug Prodcut show
    product = SlugRelatedField(slug_field='slug',queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ('product_name','product_price','status','subtotal_amount')

    def validate_order(self,value):
        """The order must will be my own """

        user = self.context['request'].user  

        if value.customer != user:
            raise ValidationError("No Order you have!")
        return value
    
    def create(self, validated_data):
        product = validated_data["product"]

        # snapshot data
        validated_data["product_name"] = product.name
        validated_data["product_price"] = product.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Customer should update ONLY quantity.
        """
        quantity = validated_data.get("quantity", instance.quantity)

        instance.quantity = quantity 
        instance.save()
        return instance
    

# ---------------------------
# Order Serializer
# ---------------------------
class OrderSerializer(ModelSerializer):
    # Nested Data
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        exclude = ('customer',) 
        read_only_fields = ('total_amount', )

