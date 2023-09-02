from django.db import models
from composite_field import CompositeField
from .si_unit_to_string import decimal_voltage_to_str, decimal_current_to_str
from ..to_string_conversions import decimal_celsius_to_str


class ForwardVoltage(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_junction_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Tj
    at_forward_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)  # IF [A]

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.min is not None or self.typ is not None or self.max is not None

        def get_display(self):
            return "{}&nbsp@IF={}, Tj={}".format(decimal_voltage_to_str(self.max),
                                                 decimal_current_to_str(self.at_forward_current),
                                                 decimal_celsius_to_str(self.at_junction_temp))

        def __str__(self):
            forward_voltage_list = [self.forward_voltage1, self.forward_voltage2, self.forward_voltage3]
            forward_voltage_str = ''
            for forward_voltage in forward_voltage_list:
                if forward_voltage:
                    if len(forward_voltage_str) > 0:
                        forward_voltage_str = forward_voltage_str + '<br>'
                    forward_voltage_str = forward_voltage_str + "{}&nbsp@IF={}, Tj={}".format(
                        decimal_voltage_to_str(forward_voltage.max),
                        decimal_current_to_str(forward_voltage.at_forward_current),
                        decimal_celsius_to_str(forward_voltage.at_junction_temp))
            return forward_voltage_str
