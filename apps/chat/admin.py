from django.contrib import admin

# Register your models here.
from .models import Message,Channel 

@admin.register(Channel)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id','order','shop','customer','is_active']

@admin.register(Message)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id']