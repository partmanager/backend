from django_filters import rest_framework as filters
from .models import DistributorOrderNumber


class DistributorOrderNumberFilter(filters.FilterSet):
    unassigned = filters.BooleanFilter(field_name='manufacturer_order_number', lookup_expr='isnull')

    class Meta:
        model = DistributorOrderNumber
        fields = ['distributor', 'manufacturer_name']

