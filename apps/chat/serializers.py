from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
# Internal
from .models import Channel, Message
# External
from apps.accounts.models import User
from apps.store.models import Shop, Product
from apps.order.models import Order,OrderItem
from apps.store.serializers import ProductListSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_role','message', 'created_at'] 
        ordering = ('-created_at',)

# ----------------------------------------
# Channle of Chat
# ----------------------------------------
class ShopSerializer(ModelSerializer):
    owner = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Shop
        fields = ('slug','name','owner','short_intro','logo')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",'email','role')

class ChannelSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    shop = ShopSerializer(read_only=True) 
    last_message = serializers.SerializerMethodField()
    order_summary = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'order', 'shop', 'customer', 'last_message','is_active','order_summary']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if not last_msg:
            return None
        return MessageSerializer(last_msg).data

    def get_order_summary(self,obj):
        # Only include order_summary for shop_owner
        user = self.context['request'].user
        order = obj.order
        shop = obj.shop

        if user.role != 'shop_owner':
            return None
        
        if not order or not shop:
            return None
    
        sub_items = OrderItem.objects.filter(order=order,product__shop=shop)  
        products = [item.product for item in sub_items]
        data = {
            'total_item_count': order.items.count(),
            'total_order_amount': order.total_amount,
            'overall_status': order.status,

            'sub_item_count': sub_items.count(),
            'sub_order_amount': sum(i.subtotal_amount for i in sub_items), 
            'products': ProductListSerializer(products, many=True).data
        }
        return data
 