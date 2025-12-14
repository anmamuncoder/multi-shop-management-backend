from django.db import models
from django.utils import timezone
import uuid 
# External
from apps.base.models import BaseModel 
from apps.accounts.models import User
# Internal
from .constrants import TRANSACTION_TYPE, TRANSACTION_STATUS

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
