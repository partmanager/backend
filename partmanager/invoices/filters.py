from django_filters import rest_framework as filters
from .models import InvoiceItem, BOOKKEEPING_TYPE
from partmanager.choices import MerchandiseType


class InvoiceItemFilter(filters.FilterSet):
    type = filters.MultipleChoiceFilter(field_name='type', choices=MerchandiseType.choices)
    bookkeeping = filters.MultipleChoiceFilter(field_name='bookkeeping', choices=BOOKKEEPING_TYPE)
    without_mon = filters.BooleanFilter(field_name="distributor_order_number__manufacturer_order_number",
                                        lookup_expr='isnull')

    class Meta:
        model = InvoiceItem
        fields = {'invoice': ['exact'],
                  'shipped_quantity': ['gt'],
                  }
