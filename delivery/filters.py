from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    item_price = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = {
            'address': ['exact', 'contains'],
            'addressee_full_name': ['exact', 'contains'],
            'city': ['exact', 'contains'],
            'phone_number': ['exact', 'contains'],
            'status': ['exact'],
            'sum': ['exact', 'lt', 'gt'],
            'client': ['exact'],
            'courier': ['exact'],
        }
