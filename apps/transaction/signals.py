from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.transaction.models import TopUp,Transaction
from apps.order.models import Order


# ----------------------------------
# Transaction TopUp Create
# ----------------------------------
@receiver(pre_save,sender=TopUp)
def make_transaction_topup(sender, instance, **kwargs):
    if not instance.pk: 
        return
    
    old = TopUp.objects.get(pk=instance.pk)
    shop_owner = instance.user.shop

    if old.status != 'success' and instance.status =='success':
        Transaction.objects.create(
            user=instance.user,
            reference=instance, 
            amount=instance.amount,
            status='success',
            transaction_type='topup',
            note="TopUp Successful"
        )
        shop_owner.balance += instance.amount
        shop_owner.save(update_fields=['balance'])

    if old.status != 'failed' and instance.status =='failed':
        Transaction.objects.create(
            user=instance.user,
            reference=instance, 
            amount=instance.amount,
            status='success',
            transaction_type='topup',
            note="TopUp Successful"
        )

# ----------------------------------
# Transaction Order Create
# ----------------------------------
@receiver(pre_save,sender=Order)
def make_transaction_order(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    old = Order.objects.get(pk=instance.pk)

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
    

    