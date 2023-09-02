from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str
from .si_unit_to_string import decimal_voltage_to_str


class BreakdownVoltage(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    at_reverse_current_uA = models.IntegerField(null=True, blank=True)  # in [uA]

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.min is not None or self.max is not None

        def __str__(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_voltage_to_str)
