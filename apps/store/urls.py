from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopView,CategoryView,ProductView,ProductImageView,ProductVariantView

routers = DefaultRouter()
routers.register('shops',ShopView)
routers.register('categories',CategoryView)
routers.register('products',ProductView)
routers.register('images',ProductImageView)
routers.register('variants',ProductVariantView)

urls_shop_owner = [
    
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
