from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_time_to_str


class FallTime(CompositeField):
    min = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    typ = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    max = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_time_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_time_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_time_to_str(self.max) if self.max else ''
