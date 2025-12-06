from django.urls import path, include
from .views import ShopView

urls_shop_owner = [
    path('shop/',ShopView.as_view(),name='shop')
]

urls_shop_customer = [

]

app_name = "store"
urlpatterns = (
    [

    ]   
    + urls_shop_owner
    + urls_shop_customer
)
