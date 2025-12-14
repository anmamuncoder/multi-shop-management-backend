from django.urls import path, include
from .views import TransactionView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('transactions',TransactionView,basename='transactions')

app_name  = "transaction"
urlpatterns = [

] + router.urls
