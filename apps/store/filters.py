from django_filters.rest_framework import FilterSet, RangeFilter,CharFilter
from .models import Shop,Category,Product,ProductImage,ProductVariant

class ProductFilter(FilterSet):
    price = RangeFilter()  # min_price & max_price query params
    category = CharFilter(field_name='category__slug', lookup_expr='exact')
    shop = CharFilter(field_name='shop__slug', lookup_expr='exact')

    class Meta:
        model = Product
        # fields = ['category']
        fields = { 
            'is_available': ['exact'], 
        }
