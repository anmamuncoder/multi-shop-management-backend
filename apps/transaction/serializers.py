from rest_framework.serializers import ModelSerializer

from .models import Transaction, AdminBankAccount,TopUp
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.transaction.models import Transaction

class ReferenceRelatedField(serializers.RelatedField):
    def to_representation(self, value): 
        if value is None:
            return None
        if hasattr(value, 'total_amount'):
            # It's an Order
            return {
                "id": str(value.id),
                "total_amount": str(value.total_amount),
                "status": value.status
            }
        elif hasattr(value, 'amount'):
            # It's a TopUp
            return {
                "id": str(value.id),
                "amount": str(value.amount),
                "status": value.status
            }
        return str(value)
 
class TransactionSerializer(ModelSerializer):
    reference = ReferenceRelatedField(read_only=True)

    class Meta:
        model = Transaction
        # fields = "__all__"
        fields = ['id', 'txn_id', 'transaction_type', 'reference','amount', 'status', 'note', 'created_at', 'updated_at']


class AdminBankAccountSerializer(ModelSerializer):
    class Meta:
        model = AdminBankAccount
        fields = "__all__"

class TopUpSerializer(ModelSerializer):
    class Meta:
        model = TopUp
        exclude = ('user',)
        read_only_fields = ['status']
