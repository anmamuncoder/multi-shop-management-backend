from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
# External
from apps.store.models import Shop
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.store.serializers import ShopCustomerSerializer
# Internal
from .models import TemplateMessage, MessageCampaign, MessageLog 

# --------------------------------
# Message Message
# --------------------------------
class TemplateMessageSerializer(ModelSerializer):
    shop = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    media = serializers.ImageField(required=False, allow_null=True)
    button = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = TemplateMessage
        fields = "__all__"
        read_only_fields = ("id",  "created_at", "updated_at")

    def validate_button(self, value):
        """Ensure button is a dict with name and valid url when provided."""
        if value in (None, {}):
            return value
        if not isinstance(value, dict):
            raise serializers.ValidationError("Button must be an object/dict.")
        if not all(k in value for k in ("name", "url")):
            raise serializers.ValidationError("Button must contain both 'name' and 'url'.")
        url = value.get("url")
        try:
            URLValidator()(url)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid URL provided in button.url")
        return value

    def validate(self, attrs):
        # If channel_to is sms, media must not be present
        channel_to = attrs.get("channel_to", getattr(self.instance, "channel_to", None))
        media = attrs.get("media", getattr(self.instance, "media", None))
        if channel_to == "sms" and media:
            raise serializers.ValidationError({"media": "SMS templates cannot contain media."})
        return attrs
    
# --------------------------------
# Message Campaign
# --------------------------------
class MessageCampaignSerializer(ModelSerializer):
    shop = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    template = serializers.PrimaryKeyRelatedField(queryset=TemplateMessage.objects.all())

    # Accept list of user IDs for write, but include nested users for read
    customers = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    customers_detail = UserSerializer(source="customers", many=True, read_only=True)

    class Meta:
        model = MessageCampaign
        fields = ("id","shop","template", "send_to","customers",'customers_detail',"scheduled_at","is_sent","snapshot_recipient_count","snapshot_cost_per_message","snapshot_total_cost","created_at","updated_at",)
        read_only_fields = ("id", "snapshot_recipient_count","snapshot_cost_per_message", "snapshot_total_cost", "created_at", "updated_at", )


    def validate_scheduled_at(self, value):
        """Validate scheduled time is in the future."""
        if value and value < timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value

    def validate(self, attrs):
        send_to = attrs.get("send_to")
        customers = attrs.get("customers")
        template = attrs.get("template")
        shop = attrs.get("shop")
        
        # Validate template belongs to shop
        if template and shop and template.shop != shop:
            raise serializers.ValidationError({"template": "Template must belong to the selected shop."})

        # Validate customers for 'selected' send_to
        if send_to == "selected" and not customers:
            raise serializers.ValidationError({"customers": "Select at least one recipient for 'selected' send_to."})
        
        return attrs

    def create(self, validated_data):
        customers = validated_data.pop("customers", None)
        # Create campaign as draft (is_sent=False)
        campaign = MessageCampaign.objects.create(**validated_data)
        # Set customers if 'selected'
        if campaign.send_to == "selected" and customers:
            campaign.customers.set(customers)
 
        return campaign  
  
# --------------------------------
# Message Log
# --------------------------------
class MessageLogSerializer(ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(queryset=MessageCampaign.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    customer_detail = UserSerializer(source="customer", read_only=True)
    class Meta:
        model = MessageLog
        fields = ("id","campaign","customer","customer_detail","status","sent_at","delivered_at","viewed_at","provider_message_id","provider_response","created_at","updated_at",)
        read_only_fields = ("id", "created_at", "updated_at")


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','email_verified')
        