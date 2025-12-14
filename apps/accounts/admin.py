from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ['username','email','role','email_verified']