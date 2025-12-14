from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Internal
from .models import Transaction,AdminBankAccount,TopUp
from .serializers import TransactionSerializer,AdminBankAccountSerializer,TopUpSerializer
# Enternal
from apps.base.paginations import BasePagination
from apps.base.permissions import IsCustomer, IsShopOwner

# Create your views here.
class TransactionView(ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination 
    lookup_field = 'txn_id'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

# ---------------------------
# Admin Bank Account
# ---------------------------
class AdminBankAccountView(ReadOnlyModelViewSet):
    serializer_class = AdminBankAccountSerializer
    queryset = AdminBankAccount.objects.all()
    permission_classes = [IsAuthenticated, IsShopOwner]

# ---------------------------
# Top Up view
# ---------------------------
class TopUpView(APIView):
    permission_classes = [IsAuthenticated,IsShopOwner]
    serializer_class = TopUpSerializer

    def get(self,request):
        user = request.user
        queryset = TopUp.objects.filter(user=user)
        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    