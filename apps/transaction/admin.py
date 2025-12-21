from django.contrib import admin, messages
from django.db import transaction as db_transaction
from .models import Transaction,AdminBankAccount,TopUp
# Register your models here.
from apps.transaction.models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id','user','amount','transaction_type','status','reference']
    
@admin.register(AdminBankAccount)
class AdminBankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number','bank_name','account_holder_name','account_holder_type','account_type','country','currency']

@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ['account_number','account_holder_name','amount','routing_number','account_type','status']
    actions = ['accept_topup']

    @admin.action(description="Accept selected TopUps")
    def accept_topup(self, request, queryset):
        queryset.update(status='success')
        