from django.contrib import admin

from .models import Transaction
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id','user','amount','transaction_type','status','reference']