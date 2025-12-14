from django.db import models
from django.utils import timezone
import uuid 
# External
from apps.base.models import BaseModel 
from apps.accounts.models import User
from apps.order.models import Order
# Internal
from .constrants import TRANSACTION_TYPE,TRANSACTION_STATUS,ACCOUNT_TYPE,CURRENCY_CHOICES

def generate_txn_id():
    today = timezone.now().strftime("%Y%m%d")
    last_txn = Transaction.objects.filter(txn_id__startswith=f"TXN-{today}").order_by("id").last()
    if last_txn:
        last_number = int(last_txn.transaction_id.split("-")[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    return f"TXN-{today}-{new_number:06d}"


# Create your models here.
class Transaction(BaseModel):
    txn_id = models.CharField(max_length=30, unique=True, editable=False )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True,related_name='transaction')

    amount = models.DecimalField(max_digits=12,decimal_places=2)

    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE)
    status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='pending')
    reference = models.CharField(max_length=255,blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.txn_id:
            self.txn_id = generate_txn_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.txn_id} | {self.user.email} | {self.amount}"

# --------------------------------
# Admin Bank Account
# --------------------------------
class AdminBankAccount(BaseModel):
    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=50)
    account_holder_type = models.CharField(max_length=15)

    account_number = models.CharField(max_length=20)
    routing_number = models.CharField(max_length=15)
    country = models.CharField(max_length=15)

    account_type  = models.CharField(max_length=10,choices=ACCOUNT_TYPE)
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES)

    def __str__(self):
        return f"{self.account_number} - {self.bank_name}"

# --------------------------------
# Top Up for shop owner
# --------------------------------
class TopUp(BaseModel): 
    # Shop Owner information
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='topups')

    bank_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    account_holder_name = models.CharField(max_length=50)

    account_number = models.CharField(max_length=20)
    routing_number = models.CharField(max_length=15)
    country = models.CharField(max_length=15)

    account_type  = models.CharField(max_length=10,choices=ACCOUNT_TYPE)
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES)
    description = models.CharField(max_length=255)

    receipt = models.ImageField(upload_to="topups/")
    
    status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='pending')

    def __str__(self):
        return f"ACC - {self.account_number} - {self.status}"

