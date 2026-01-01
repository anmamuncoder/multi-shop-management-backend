from django.contrib import admin
from .models import TemplateMessage, MessageCampaign, MessageLog, MessagePlan
# Register your models here.

@admin.register(TemplateMessage)
class TemplateMessageAdmin(admin.ModelAdmin):
    list_display = ("title", "shop", "message_type", "status", "is_active")
    list_filter = ("message_type", "status", "shop")
    search_fields = ("title",)


@admin.register(MessageCampaign)
class MessageCampaignAdmin(admin.ModelAdmin):
    list_display = ("template", "shop", "send_to", "is_sent", "scheduled_at")
    list_filter = ("send_to", "shop", "is_sent")
    filter_horizontal = ("customers",)


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("campaign", "customer", "status", "sent_at", "viewed_at")
    list_filter = ("status",)
    search_fields = ("customer__username",)


@admin.register(MessagePlan)
class MessagePlanAdmin(admin.ModelAdmin):
    list_display = ("name",'send_to','price','cost_per_message','is_active')

