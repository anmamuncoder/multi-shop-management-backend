from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

from apps.order.models import Order,OrderItem
from .models import Channel

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

@receiver(pre_save, sender=Order)
def make_channel_off(sender, instance, **kwargs):
    """
    After Order delevered or cancelled autmaticaly will close the chat channel
    """
    old_order = Order.objects.get(pk=instance.pk)
    new_order = instance
    shops = set([i.product.shop for i in new_order.items.all()])

    if old_order.status not in ['delivered', 'cancelled'] and instance.status in ['delivered', 'cancelled']:
        Channel.objects.filter(order=new_order, shop__in=shops).update(is_active=False)