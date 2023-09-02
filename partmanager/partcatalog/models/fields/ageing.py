from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_ppm_to_str, decimal_celsius_to_str


class Ageing(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def get_min_display(self):
            return decimal_ppm_to_str(self.min) + '/year' if self.min else ''

        def get_typ_display(self):
            return decimal_ppm_to_str(self.typ) + '/year' if self.typ else ''

        def get_max_display(self):
            return decimal_ppm_to_str(self.max) + '/year' if self.max else ''

        def get_condition_display(self):
            return "T<sub>A</sub>={}".format(decimal_celsius_to_str(self.at_temp))