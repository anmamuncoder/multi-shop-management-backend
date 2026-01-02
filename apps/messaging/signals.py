from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from django.contrib.contenttypes.models import ContentType

from apps.transaction.models import Transaction
from .models import MessageCampaign

@receiver(pre_save, sender=MessageCampaign)
def create_transaction_on_send(sender, instance, **kwargs):
    """
    Create a Transaction only when is_sent changes from False -> True.
    """
    if instance._state.adding:
        # New campaign being created - skip
        return

    # Fetch previous value from DB
    previous = sender.objects.get(pk=instance.pk)

    if not previous.is_sent and instance.is_sent:
        shop = instance.shop

        # Get content type for GenericForeignKey
        content_type = ContentType.objects.get_for_model(instance)

        # Check if transaction already exists for this instance
        if not Transaction.objects.filter(content_type=content_type, object_id=instance.pk).exists():
            with db_transaction.atomic():
                Transaction.objects.create(
                    user=shop.owner,
                    reference=instance,
                    amount=instance.snapshot_total_cost,
                    status='success',
                    transaction_type='promotion',
                    note=f"Message campaign '{instance.template.title}' sent"
                )
