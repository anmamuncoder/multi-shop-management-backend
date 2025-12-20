from rest_framework.serializers import Serializer, ModelSerializer, SlugRelatedField, SerializerMethodField
# Internal
from .models import Order, OrderItem
from apps.store.models import Product, ProductVariant
from rest_framework.exceptions import ValidationError 

# ---------------------------
# Order Item Serializer
# ---------------------------
class ProductVariantSerializer(ModelSerializer): 
    class Meta:
        model = ProductVariant
        fields = ('id','title','value','extra_price','sku')

class OrderItemSerializer(ModelSerializer):
    # Slug Prodcut show
    product = SlugRelatedField(slug_field='slug',queryset=Product.objects.all())
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ('product_name','product_price','subtotal_amount')

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
        validated_data["product_image"] = product.images.filter(is_primary=True).first().image.url if product.images.exists() else None

        return super().create(validated_data)
 
    def update(self, instance, validated_data):
        """
        Customer should update ONLY quantity.
        """
        user = self.context['request'].user

        if user.role == "customer":
            # Customer can only update quantity
            instance.quantity = validated_data.get("quantity", instance.quantity)
        elif user.role == "shop_owner":
            # Shop owner can only update status
            instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance
    
from django.db.models import Sum
# ---------------------------
# Order Serializer
# ---------------------------
class OrderSerializer(ModelSerializer):
    # Nested Data 
    items = SerializerMethodField()
    total_amount = SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('customer',) 
        read_only_fields = ('total_amount', )

    def get_items(self,obj):
        user = getattr(self.context.get("request"), "user", None) 
        qs = obj.items.all()

        # Shop owner will view only his own items list
        if user and user.is_authenticated and user.role == 'shop_owner':
            qs = qs.filter(product__shop__owner=user)

        return OrderItemSerializer(qs, many=True).data

    def get_total_amount(self, obj):
        user = getattr(self.context.get("request"), "user", None)

        if not user or not user.is_authenticated:
            return obj.total_amount

        # Customer sees full order total
        if user.role == "customer":
            return obj.total_amount

        # Shop owner sees subtotal of his items only
        if  user.role == "shop_owner":
            total = (obj.items.filter(product__shop__owner=user).aggregate(total=Sum("subtotal_amount")).get("total") )
            return total or 0

        return obj.total_amount