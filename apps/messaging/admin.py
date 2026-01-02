from django.contrib import admin
from .models import (
    TemplateMessage,
    MessageCampaign,
    MessageLog,
    MessagePlan
)

# --------------------------------
# Template Message Admin
# --------------------------------
@admin.register(TemplateMessage)
class TemplateMessageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "shop",
        "channel_to",
        "status",
        "is_active",
        "created_at",
    )
    list_filter = ("channel_to", "status", "is_active", "shop")
    search_fields = ("title", "body")
    ordering = ("-created_at",)
    list_select_related = ("shop",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("shop", "title", "body")
        }),
        ("Message Configuration", {
            "fields": ("channel_to", "status", "is_active")
        }),
        ("Media & Extra", {
            "fields": ("media", "footer", "button"),
            "classes": ("collapse",),
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at", "updated_at")


# --------------------------------
# Message Campaign Admin
# --------------------------------
@admin.register(MessageCampaign)
class MessageCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "template",
        "shop",
        "send_to",
        "channel_to",
        "is_sent",
        "scheduled_at",
        "snapshot_total_cost",
    )
    list_filter = ("send_to", "channel_to", "is_sent", "shop")
    search_fields = ("template__title",)
    ordering = ("-scheduled_at",)
    list_select_related = ("shop", "template")

    autocomplete_fields = ("template",)

    fieldsets = (
        ("Campaign Info", {
            "fields": ("shop", "template", "send_to", "customers")
        }),
        ("Schedule & Status", {
            "fields": ("scheduled_at", "is_sent")
        }),
        ("Snapshot (Read Only)", {
            "fields": (
                "channel_to",
                "snapshot_recipient_count",
                "snapshot_cost_per_message",
                "snapshot_total_cost",
            )
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = (
        "channel_to",
        "snapshot_recipient_count",
        "snapshot_cost_per_message",
        "snapshot_total_cost",
        "created_at",
        "updated_at",
    )


# --------------------------------
# Message Log Admin
# --------------------------------
@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = (
        "campaign",
        "customer",
        "status",
        "sent_at",
        "delivered_at",
        "viewed_at",
    )
    list_filter = ("status",)
    search_fields = ("customer__username", "campaign__template__title")
    ordering = ("-created_at",)
    list_select_related = ("campaign", "customer")

    readonly_fields = (
        "provider_message_id",
        "provider_response",
        "created_at",
        "updated_at",
    )


# --------------------------------
# Message Plan Admin
# --------------------------------
@admin.register(MessagePlan)
class MessagePlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "send_to",
        "channel_to",
        "price",
        "cost_per_message",
        "daily_limit",
        "is_active",
    )
    list_filter = ("send_to", "channel_to", "is_active")
    search_fields = ("name",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Plan Details", {
            "fields": ("name", "description")
        }),
        ("Message Rules", {
            "fields": ("send_to", "channel_to", "daily_limit")
        }),
        ("Pricing", {
            "fields": ("price", "cost_per_message")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at", "updated_at")
