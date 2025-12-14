from django.urls import path, include
from .views import TransactionView,AdminBankAccountView,TopUpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('transactions',TransactionView,basename='transactions')

meta_router = DefaultRouter()
meta_router.register('bank',AdminBankAccountView)

app_name  = "transaction"
urlpatterns = [
    path('meta/',include(meta_router.urls)),

    path('topups/',TopUpView.as_view(),name='topups')

] + router.urls
