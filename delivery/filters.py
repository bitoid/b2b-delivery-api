from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, CharFilter, NumberFilter
from .models import Order
from django_filters.filters import Filter
from datetime import datetime, timedelta

class ListFilter(BaseInFilter, CharFilter):
    pass

class NullableNumberInFilter(BaseInFilter, NumberFilter):
    def filter(self, qs, value):
        if value:
            if 'null' in value:
                value.remove('null')
                qs = qs.filter(**{
                    f"{self.field_name}__isnull": True
                })
            if value:
                qs = super().filter(qs, value)
        return qs
    

class DateRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            dates = [v.strip() for v in value.split('to')]
            if len(dates) == 2:
                start_date_str, end_date_str = dates
                if start_date_str and end_date_str:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

                    end_date += timedelta(days=1)

                    start_lookup = f'{self.field_name}__gte'
                    end_lookup = f'{self.field_name}__lt' 
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
    client = NullableNumberInFilter(field_name='client__id')
    courier = NullableNumberInFilter(field_name='courier__id')
    created_at = DateRangeFilter()
    item_price = RangeFilter()

    class Meta:
        model = Order
        fields = []

    def filter_queryset(self, queryset):
        queryset = super(OrderFilter, self).filter_queryset(queryset)
        field = self.data.get('field', None)
        order = self.data.get('order', None)

        if field in ['created_at', 'item_price', 'courier_fee'] and order:
            if order == 'ascend':
                queryset = queryset.order_by(field)
            elif order == 'descend':
                queryset = queryset.order_by(f'-{field}')
        return queryset

    class Meta:
        model = Order
        fields = []

