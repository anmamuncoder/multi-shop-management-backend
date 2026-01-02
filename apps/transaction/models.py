from django.db import models
from django.utils import timezone
import uuid 
# External
from apps.base.models import BaseModel 
from apps.accounts.models import User
from apps.order.models import Order
# Internal
from .constrants import TRANSACTION_TYPE,TRANSACTION_STATUS,ACCOUNT_TYPE,CURRENCY_CHOICES
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import random

def generate_txn_id():
    today = timezone.now().strftime("%Y%m%d%H%M%S%f")
    rand = random.randint(100, 999)
    return f"TXN-{today}-{rand}"

# Create your models here.
class Transaction(BaseModel):
    txn_id = models.CharField(max_length=30, unique=True, editable=False )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE,default='order')

    # Multiple reference
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True,limit_choices_to=Q(model__in=['order', 'topup','messagecampaign']))
    object_id = models.UUIDField(null=True)
    reference = GenericForeignKey('content_type', 'object_id')

    amount = models.DecimalField(max_digits=12,decimal_places=2)
    status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='pending')
    note = models.CharField(max_length=255,blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.txn_id:
            self.txn_id = generate_txn_id()
        super().save(*args, **kwargs)

    def clean(self):
        allowed_models = ('order', 'topup','messagecampaign')
        if self.content.model not in allowed_models:
            raise ValidationError(f"Transaction can only reference {allowed_models}")
        
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

