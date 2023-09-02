from decimal import Decimal
from django.db import models
from composite_field import CompositeField
from .si_unit_to_string import decimal_voltage_to_str
from ..to_string_conversions import decimal_capacitance_to_str


class JunctionCapacitance(CompositeField):
    min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    typ = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=7, decimal_places=0, null=True, blank=True)  # Tj
    at_reverse_voltage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # V_R

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def typ_in_farads(self):
            return self.typ / Decimal('1e12')

        def max_in_farads(self):
            return self.max / Decimal('1e12')

        def __str__(self):
            if self.capacitance_in_pf:
                vr = decimal_voltage_to_str(self.capacitance_in_pf.at_reverse_voltage)
                frequency = self.capacitance_in_pf.at_frequency / 1000000
                if self.capacitance_in_pf.typ:
                    return "{}&nbsp@VR={}, f={}MHz".format(
                        decimal_capacitance_to_str(self.typ_in_farads()), vr, frequency)
                else:
                    return "max&nbsp{}&nbsp@VR={}, f={}MHz".format(
                        decimal_capacitance_to_str(self.max_in_farads()), vr, frequency)
