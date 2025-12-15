from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

from .models import Order, OrderItem
from apps.transaction.models import Transaction
from apps.chat.models import Channel

@receiver(pre_save,sender=Order)
def make_transaction_order(sender, instance, **kwargs):

    if instance._state.adding:
        return

    old = Order.objects.get(pk=instance.pk)

    # ---------------------------------- 
    # After Order delevered or cancelled autmaticaly will close the chat channel
    # ----------------------------------  

    if old.status not in ['delivered', 'cancelled'] and instance.status in ['delivered', 'cancelled']:
        shops = set([i.product.shop for i in instance.items.all()])
        Channel.objects.filter(order=instance, shop__in=shops).update(is_active=False)

    # ----------------------------------
    # Transaction Order Create
    # ---------------------------------- 
    if old.status != 'delivered' and instance.status =='delivered':
        Transaction.objects.create(
            user=instance.customer,
            reference=instance, 
            amount=instance.total_amount,
            status='success',  
            note="Order delivered Successful"
        )
    if old.status != 'cancelled' and instance.status =='cancelled':
        Transaction.objects.create(
            user=instance.customer,
            reference=instance, 
            amount=instance.total_amount,
            status='failed',  
            note="Order cancelled"
        )
    

@receiver(post_save,sender=OrderItem)
def make_channel_create(sender, instance, created, **kwargs):
    """
    After Any item include any order automaticaly will create channel to chat customer with shop_owner
    """
    if created:
        order = instance.order
        shop = instance.product.shop
        customer = order.customer
        Channel.objects.get_or_create(order=order, shop=shop, customer=customer)

 