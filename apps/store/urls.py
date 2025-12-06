from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopView,CategoryView

routers = DefaultRouter()
routers.register('category',CategoryView)

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
    + routers.urls
)
