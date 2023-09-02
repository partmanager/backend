from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str
from .si_unit_to_string import decimal_inductance_to_str, decimal_frequency_to_str
from ..to_string_conversions import decimal_celsius_to_str


class InductanceAtFrequencyAtTemp(CompositeField):
    min = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    typ = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    max = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    at_frequency = models.IntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            value = min_typ_max_to_str(self.min, self.typ, self.max, decimal_inductance_to_str)
            if self.at_frequency or self.at_temp:
                value = value + " @"
            if self.at_frequency:
                value = value + " " + decimal_frequency_to_str(self.at_frequency)
            if self.at_temp:
                value = value + " " + decimal_celsius_to_str(self.at_temp)
            return value
