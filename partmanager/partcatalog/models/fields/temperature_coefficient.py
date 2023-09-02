from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str


def decimal_ppm_to_str(value):
    return "{} ppm/°C".format(value)


class TemperatureCoefficient(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in ppm/K
    typ = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in ppm/K
    max = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in ppm/K

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_ppm_to_str)

        def get_min_display(self):
            return decimal_ppm_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_ppm_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_ppm_to_str(self.max) if self.max else ''
