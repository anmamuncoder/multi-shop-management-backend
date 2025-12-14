from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Internal
from .models import Transaction
from .serializers import TransactionSerializer
# Enternal
from apps.base.paginations import BasePagination

# Create your views here.
class TransactionView(ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination 
    lookup_field = 'txn_id'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
