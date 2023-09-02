from django.db import models
from composite_field import CompositeField
from ..choices import MSLevel
from ..to_string_conversions import decimal_celsius_to_str


class StorageConditions(CompositeField):
    temperature_min = models.IntegerField(null=True, blank=True)
    temperature_max = models.IntegerField(null=True, blank=True)
    humidity_min = models.IntegerField(null=True, blank=True)  # %
    humidity_max = models.IntegerField(null=True, blank=True)  # %
    msl_level = models.IntegerField(choices=MSLevel.choices, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def to_ajax(self):
            return {
                'temperature_min': self.temperature_min,
                'temperature_max': self.temperature_max,
                'humidity_min': self.humidity_min,
                'humidity_max': self.humidity_max,
                'msl': self.msl_level
            }
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            if self.temperature_min is None and self.temperature_max is None:
                return '-'
            if self.msl_level is not None:
                return "{}..{}, MSL {}".format(decimal_celsius_to_str(self.temperature_min),
                                               decimal_celsius_to_str(self.temperature_max),
                                               self.msl_level)
            else:
                return "{}..{}".format(decimal_celsius_to_str(self.temperature_min),
                                       decimal_celsius_to_str(self.temperature_max))
