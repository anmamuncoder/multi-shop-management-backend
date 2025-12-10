from django.db import models

# Create your models here.
from apps.store.models import Shop,Product,Category,ProductImage,ProductVariant
from apps.order.models import Order,OrderItem
from apps.base.models import BaseModel
from apps.accounts.models import User

class Channel(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='channels')
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='channels')
    customer = models.ForeignKey(User,limit_choices_to={'role':'customer'},on_delete=models.CASCADE,related_name='channels')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.order.id} Shop {self.shop.slug}"
    
class Message(BaseModel):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.sender.email} - {self.room.id} - {self.created_at}"
    