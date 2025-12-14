from django.contrib import admin

from .models import Transaction,AdminBankAccount,TopUp
# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['txn_id','user','amount','transaction_type','status','reference']
    
@admin.register(AdminBankAccount)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account_number','bank_name','account_holder_name','account_holder_type','account_type','country','currency']

@admin.register(TopUp)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account_number','account_holder_name','amount','routing_number','account_type','status']