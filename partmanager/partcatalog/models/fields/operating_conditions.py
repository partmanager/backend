from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_celsius_to_str


class OperatingConditions(CompositeField):
    temperature_min = models.IntegerField(null=True, blank=True)
    temperature_max = models.IntegerField(null=True, blank=True)
    humidity_min = models.IntegerField(null=True, blank=True)  # %
    humidity_max = models.IntegerField(null=True, blank=True)  # %

    class Proxy(CompositeField.Proxy):
        def to_dict(self):
            return {
                'temperature_min': self.temperature_min,
                'temperature_max': self.temperature_max,
                'humidity_min': self.humidity_min,
                'humidity_max': self.humidity_max,
            }

        def __str__(self):
            if self.temperature_min is None and self.temperature_max is None:
                return '-'
            else:
                return "{}..{}".format(decimal_celsius_to_str(self.temperature_min),
                                       decimal_celsius_to_str(self.temperature_max))
