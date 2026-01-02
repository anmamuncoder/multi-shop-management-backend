from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, MaxLengthValidator
# External
from apps.store.models import Shop
from apps.base.models import BaseModel 
# Internal
from .constants import MESSAGE_STATUS, MESSAGE_TYPE, MESSAGE_LOG_STATUS, SEND_TO_CHOICES
from decimal import Decimal
# Create your models here. 
# --------------------------------
# Message Message
# --------------------------------
class TemplateMessage(BaseModel):  
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name="template_messages")

    title = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)

    channel_to = models.CharField(max_length=20,choices=MESSAGE_TYPE,default='push')
    status = models.CharField(max_length=20,choices= MESSAGE_STATUS,default='active')
    media = models.ImageField(upload_to="template_media/",null=True,blank=True)
    footer = models.CharField(max_length=200,null=True,blank=True)

    # Button stored as structured JSON
    button = models.JSONField(null=True,blank=True,default=dict,
        help_text="""
        Example:
        {
            "name": "View Order",
            "url": "https://example.com/order/123"
        }
        """
    )  
    # If it will be Campain then will be active=True
    is_active = models.BooleanField(default=False) 

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["shop",]),
            models.Index(fields=["channel_to", "status"]),
        ]
 
    def clean(self):
        if not isinstance(self.button, dict):
            raise ValidationError({"button": "Button must be an object/dict."})
        if self.button:
            if not all(k in self.button for k in ("name", "url")):
                raise ValidationError("Button must contain both 'name' and 'url'." )
        try:
            URLValidator()(self.button.get("url"))
        except ValidationError:
            raise ValidationError({"button": "Invalid URL in button."})
        
        if self.message_type == 'sms' and self.media:
            raise ValidationError("SMS templates cannot contain media.")

    def __str__(self):
        return f"{self.title} ({self.message_type})"

 
# --------------------------------
# Message Campaign
# --------------------------------
class MessageCampaign(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,related_name="message_campaigns")
    template = models.ForeignKey(TemplateMessage,on_delete=models.CASCADE,related_name="campaigns")

    send_to = models.CharField(max_length=20, choices=SEND_TO_CHOICES)
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="message_campaigns")

    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    # Snapshot fields (IMPORTANT)
    channel_to = models.CharField(max_length=20,choices=MESSAGE_TYPE,editable=False,null=True) 
    snapshot_recipient_count = models.PositiveIntegerField(default=0,editable=False)
    snapshot_cost_per_message = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"),editable=False)
    snapshot_total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"),editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["scheduled_at"]),
            models.Index(fields=["is_sent"]),
        ]
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.template.title} - {self.send_to}"

 
# --------------------------------
# Message Log
# --------------------------------
class MessageLog(BaseModel):
    campaign = models.ForeignKey(MessageCampaign,on_delete=models.CASCADE,related_name="logs")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    status = models.CharField(max_length=20,choices=MESSAGE_LOG_STATUS,default="pending")

    sent_at = models.DateTimeField(null=True, blank=True)

    delivered_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(null=True, blank=True)

    provider_message_id = models.CharField(max_length=255,null=True,blank=True)
    provider_response = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["campaign", "customer"], name="unique_campaign_and_customer")
        ]  

# --------------------------------
# Message Plan
# --------------------------------
class MessagePlan(BaseModel): 
    name = models.CharField(max_length=100, help_text="Plan name e.g. Basic, Pro")
    description = models.TextField(help_text="Feature Description write saparately with comma") 
    
    send_to = models.CharField(max_length=20, choices=SEND_TO_CHOICES)
    channel_to = models.CharField(max_length=20,choices=MESSAGE_TYPE,default='push',null=True) 

    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("1.20"))
    cost_per_message = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("1.20"))
    
    daily_limit = models.PositiveIntegerField(default=1000, help_text="Max messages shop can send per day")

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['send_to','is_active'],name="only_one_active_send_method")
        ]

    def __str__(self):
        return f"{self.name} (${self.cost_per_message}/msg)"
