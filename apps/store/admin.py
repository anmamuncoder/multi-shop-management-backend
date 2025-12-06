from django.contrib import admin

# Register your models here.
from .models import Shop,Category,Product,ProductImage,ProductVariant

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('owner','name','is_active','is_verified','created_at')
    # prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('shop','name','is_active','created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('shop','category','name','sku','stock_quantity','cost_price','tags','created_at')
@admin.register(ProductImage)
class RroductImageAdmin(admin.ModelAdmin):
    list_display = ('product','alt_text','sort_order','is_primary','created_at')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product','title','value','sku','stock_quantity','extra_price','created_at')

