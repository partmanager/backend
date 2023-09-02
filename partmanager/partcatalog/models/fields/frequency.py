from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str
from ..to_string_conversions import decimal_frequency_to_str, decimal_ppm_to_str, decimal_celsius_to_str


class Frequency(CompositeField):
    min = models.BigIntegerField(null=True, blank=True)
    typ = models.BigIntegerField(null=True, blank=True)
    max = models.BigIntegerField(null=True, blank=True)
    tolerance_ppm = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    at_temp_tolerance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            if self.tolerance_ppm:
                value_str = "{} ±{}".format(decimal_frequency_to_str(self.typ), decimal_ppm_to_str(self.tolerance_ppm))
            else:
                value_str = min_typ_max_to_str(self.min, self.typ, self.max, decimal_frequency_to_str)
            return value_str

        def get_min_display(self):
            return decimal_frequency_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_frequency_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_frequency_to_str(self.max) if self.max else ''

        def get_tolerance_ppm_display(self):
            return '±' + decimal_ppm_to_str(self.tolerance_ppm) if self.tolerance_ppm else ''

        def get_tolerance_ppm_condition_display(self):
            return "T<sub>A</sub>={} {}".format(decimal_celsius_to_str(self.at_temp),
                                                '±' + decimal_celsius_to_str(
                                                    self.at_temp_tolerance) if self.at_temp_tolerance else '')

        def get_condition_display(self):
            return "T<sub>A</sub>={}".format(decimal_celsius_to_str(self.at_temp))
