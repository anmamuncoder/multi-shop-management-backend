from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import OrderView, OrderItemView

router = DefaultRouter()
router.register('orders',OrderView,basename="orders")
router.register('items',OrderItemView,basename="items")

app_name = "order"
urlpatterns = (
    [

    ]
    +   router.urls
)
