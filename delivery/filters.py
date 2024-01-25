from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, CharFilter, NumberFilter
from .models import Order
import django_filters

class ListFilter(BaseInFilter, CharFilter):
    pass

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class DateRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            dates = [v.strip() for v in value.split('to')]
            if len(dates) == 2:
                start_date, end_date = dates
                if start_date and end_date:
                    start_lookup = f'{self.field_name}__gte'
                    end_lookup = f'{self.field_name}__lte'
                    return qs.filter(**{start_lookup: start_date, end_lookup: end_date})
        return qs


class OrderFilter(filters.FilterSet):
    address = ListFilter()
    addressee_full_name = ListFilter()
    city = ListFilter()
    phone_number = ListFilter()
    status = ListFilter()
    client = NumberInFilter(field_name='client__id')
    courier = NumberInFilter(field_name='courier__id')
    created_at = DateRangeFilter()
    item_price = filters.RangeFilter()

    class Meta:
        model = Order
        fields = []
