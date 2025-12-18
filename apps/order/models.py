from django.db import models
# Internal
from .constants import ORDER_STATUS,ORDER_ITEM_STATUS
# External
from apps.base.models import BaseModel
from apps.accounts.models import User
from apps.store.models import Shop,Category,Product,ProductImage,ProductVariant

# Create your models here.
class Order(BaseModel):
    customer = models.ForeignKey(User,on_delete=models.PROTECT, limit_choices_to={'role':'customer'} ,related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(choices=ORDER_STATUS, max_length=20, default='pending')
    
    # Shipping Address  
    shipping_street_address  = models.TextField(blank=True,null=True)
    shipping_city = models.CharField(max_length=100,blank=True,null=True)
    shipping_state = models.CharField(max_length=100,blank=True,null=True)
    shipping_postal_code = models.CharField(max_length=20,blank=True,null=True)
    shipping_country = models.CharField(max_length=100,blank=True, default="Bangladesh",null=True)

    def update_total(self):
        total = sum(i.subtotal_amount for i in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Order - {self.customer.email}"

        
class OrderItem(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="orderitems",null=True)

    quantity = models.PositiveIntegerField()
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    # Snapshot fields
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.URLField(null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='orderitems',null=True)

    status = models.CharField(choices=ORDER_ITEM_STATUS, max_length=20, default="pending")

    def save(self, *args, **kwargs):
        sub_total  = self.product_price * (self.quantity or 1)
        # extra variant price
        if self.product_variant and self.product_variant.extra_price:
            sub_total += self.product_variant.extra_price
            
        self.subtotal_amount = sub_total
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f"Order Item - {self.product_name} - {self.quantity}"
    