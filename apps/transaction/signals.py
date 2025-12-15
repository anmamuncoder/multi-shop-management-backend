from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.transaction.models import TopUp,Transaction
from apps.order.models import Order


# ----------------------------------
# Transaction TopUp Create
# ----------------------------------
@receiver(pre_save,sender=TopUp)
def make_transaction_topup(sender, instance, **kwargs):
    # if not instance.pk: 
    #     return
    if instance._state.adding:
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

