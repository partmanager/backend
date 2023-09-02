from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_celsius_to_str
from .si_unit_to_string import decimal_current_to_str


class MaxCurrentAtTemp(CompositeField):
    max = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def get_value_display(self):
            return self.get_voltage_display()

        def get_current_display(self):
            if self.max is not None:
                return "max. {}".format(decimal_current_to_str(self.max))
            return ''

        def get_condition_display(self):
            if self.at_temp is not None:
                return decimal_celsius_to_str(self.at_temp)

        def __bool__(self):
            return self.max is not None

        def __str__(self):
            if self.at_temp is not None:
                return "{} @ {}".format(self.get_current_display(), self.get_condition_display())
            return self.get_current_display()


class MaxCurrentAtTempAtFreq(CompositeField):
    max = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    at_freq = models.BigIntegerField(null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None
