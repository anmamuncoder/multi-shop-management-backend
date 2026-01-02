from decimal import Decimal
from typing import List
from django.db import transaction
from rest_framework.serializers import ValidationError
# External
from apps.messaging.models import MessageCampaign, MessagePlan, MessageLog
from apps.store.models import Shop
from apps.accounts.models import User
# Utils
from apps.messaging.utils import (
    send_bulk_email,
    send_push_notifications,
    send_whatsapp_messages,
    send_sms_messages
)

class MessageCampaignService: 
    @staticmethod
    def get_active_plan(send_to, channel_to='push') -> MessagePlan:
        plan = MessagePlan.objects.filter(send_to=send_to, channel_to=channel_to, is_active=True).first()
        if not plan:
            raise ValidationError(f"No active MessagePlan found for send_to: {send_to}, channel_to: {channel_to}")
        return plan

    @staticmethod
    def get_recipient_ids(campaign: MessageCampaign) -> List[int]:
        if campaign.send_to == "selected":
            return list(campaign.customers.values_list("id", flat=True))
        if campaign.send_to == "all":
            return list(User.objects.filter(role="customer").values_list("id", flat=True))
        return []

    @staticmethod
    def get_new_recipients(campaign: MessageCampaign, recipient_ids: List[int]) -> List[int]:
        existing_ids = set(
            MessageLog.objects.filter(campaign=campaign, customer_id__in=recipient_ids)
            .values_list("customer_id", flat=True)
        )
        return [rid for rid in recipient_ids if rid not in existing_ids]

    @staticmethod
    def calculate_cost(plan: MessagePlan, recipient_count: int) -> Decimal:
        return (plan.cost_per_message or Decimal("0")) * Decimal(recipient_count)

    @staticmethod
    def deduct_shop_balance(shop: Shop, total_cost: Decimal):
        with transaction.atomic():
            shop = Shop.objects.select_for_update().get(id=shop.id)
            if shop.balance < total_cost:
                raise ValidationError(f"Insufficient balance. Required: {total_cost}, Available: {shop.balance}")
            shop.balance -= total_cost
            shop.save(update_fields=["balance", "updated_at"])

    @classmethod
    def handle_campaign(cls, campaign: MessageCampaign) -> dict:
        plan = cls.get_active_plan(campaign.send_to, campaign.channel_to)
        recipient_ids = cls.get_recipient_ids(campaign)

        if not recipient_ids:
            return False, {"charged_count": 0, "total_cost": Decimal("0"), "message": "No recipients"}

        new_recipient_ids = cls.get_new_recipients(campaign, recipient_ids)
        if not new_recipient_ids:
            return False, {"charged_count": 0, "total_cost": Decimal("0"), "message": "All recipients already processed"}

        total_cost = cls.calculate_cost(plan, len(new_recipient_ids))
        cls.deduct_shop_balance(campaign.shop, total_cost)

        # Fetch User objects
        users = list(User.objects.filter(id__in=new_recipient_ids))

        # Send messages based on channel
        if campaign.channel_to == "email":
            send_bulk_email(campaign, users)
        elif campaign.channel_to == "push":
            send_push_notifications(campaign.template, users)
        elif campaign.channel_to == "whatsapp":
            send_whatsapp_messages(campaign.template, users)
        elif campaign.channel_to == "sms":
            send_sms_messages(campaign.template, users)
        else:
            raise ValidationError(f"Unsupported channel: {campaign.channel_to}")
        
        # Create MessageLogs
        logs_to_create = [MessageLog(campaign=campaign, customer=user) for user in users]
        MessageLog.objects.bulk_create(logs_to_create)

        return True, {
            "charged_count": len(users),
            "total_cost": total_cost,
            "message": f"Campaign sent to {len(users)} recipients via {campaign.channel_to.upper()}"
        }

    @classmethod
    def process_campaign(cls, campaign: MessageCampaign) -> dict:
        return cls.handle_campaign(campaign)
