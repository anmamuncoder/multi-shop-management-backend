from rest_framework.serializers import ModelSerializer

from .models import Transaction, AdminBankAccount,TopUp

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class AdminBankAccountSerializer(ModelSerializer):
    class Meta:
        model = AdminBankAccount
        fields = "__all__"

class TopUpSerializer(ModelSerializer):
    class Meta:
        model = TopUp
        exclude = ('user',)
        read_only_fields = ['status']
