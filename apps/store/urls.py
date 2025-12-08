from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopView,CategoryView,ProductView,ProductImageView,ProductVariantView

routers = DefaultRouter()
routers.register('shops',ShopView, basename="shops")
routers.register('categories',CategoryView,basename='categories')
routers.register('products',ProductView,basename='products')
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
