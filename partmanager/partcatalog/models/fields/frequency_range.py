from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_frequency_to_str
from .min_typ_max_field_to_str import min_typ_max_to_str


class FrequencyRange(CompositeField):
    min = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.min is not None or self.max is not None

        def get_min_display(self):
            return decimal_frequency_to_str(self.min) if self.min else ''

        def get_max_display(self):
            return decimal_frequency_to_str(self.max) if self.max else ''

        def __str__(self):
            return min_typ_max_to_str(self.min, None, self.max, decimal_frequency_to_str)
