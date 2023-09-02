from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_voltage_to_str
from .min_typ_max_field_to_str import min_typ_max_to_str


class SupplyVoltageRange(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_supply_voltage_display(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_voltage_to_str)

        def __str__(self):
            return self.get_supply_voltage_display()
