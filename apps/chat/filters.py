from django_filters import rest_framework as filters
from .models import Channel

class ChannelFilter(filters.FilterSet):
    order = filters.UUIDFilter(field_name="order", lookup_expr="exact")
    shop = filters.CharFilter(field_name="shop__slug", lookup_expr="iexact")

    class Meta:
        model = Channel
        fields = ['order', 'shop']
