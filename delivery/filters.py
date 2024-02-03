from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, CharFilter, NumberFilter
from .models import Order
from django_filters.filters import Filter

class ListFilter(BaseInFilter, CharFilter):
    pass

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class CustomOrderingFilter(Filter):
    def filter(self, qs, value):
        if value == 'ascend':
            return qs.order_by('created_at')
        elif value == 'descend':
            return qs.order_by('-created_at')
        return qs

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


class RangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            range_values = [v.strip() for v in value.split('to')]
            if len(range_values) == 2:
                min_value, max_value = range_values
                if min_value.isdigit() and max_value.isdigit():
                    min_lookup = f'{self.field_name}__gte'
                    max_lookup = f'{self.field_name}__lte'
                    return qs.filter(**{min_lookup: min_value, max_lookup: max_value})
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
    item_price = RangeFilter()
    order = CustomOrderingFilter(method='filter_order')

    def filter_order(self, queryset, name, value):
        if value == 'ascend':
            return queryset.order_by('created_at')
        elif value == 'descend':
            return queryset.order_by('-created_at')
        return queryset

    class Meta:
        model = Order
        fields = []
