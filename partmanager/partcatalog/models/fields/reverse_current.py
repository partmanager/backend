from django.db import models
from composite_field import CompositeField
from .si_unit_to_string import decimal_voltage_to_str, decimal_current_to_str
from ..to_string_conversions import decimal_celsius_to_str


class ReverseCurrent(CompositeField):
    symbol = 'I_R'
    min = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    at_junction_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Tj
    at_ambient_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # T_A
    at_reverse_voltage = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # V_R

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None

        def __str__(self):
            reverse_current_list = [self.reverse_current1, self.reverse_current2, self.reverse_current3,
                                    self.reverse_current4]
            reverse_current_str = ''
            for reverse_current in reverse_current_list:
                if reverse_current:
                    if len(reverse_current_str) > 0:
                        reverse_current_str = reverse_current_str + '<br>'
                    reverse_current_str = reverse_current_str + "{}&nbsp@VR={}, Tj={}".format(
                        decimal_current_to_str(reverse_current.max),
                        decimal_voltage_to_str(reverse_current.at_reverse_voltage),
                        decimal_celsius_to_str(reverse_current.at_junction_temp))
            return reverse_current_str


class MaxReverseCurrent(CompositeField):
    symbol = 'I_R'
    max = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    at_junction_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Tj
    at_reverse_voltage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # V_R

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None