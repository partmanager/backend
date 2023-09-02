from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str
from .si_unit_to_string import decimal_impedance_to_str
from .si_unit_to_string import decimal_frequency_to_str


class ImpedanceAtFreq(CompositeField):
    min = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    typ = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    max = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    tolerance = models.IntegerField(null=True, blank=True)  # %
    at_frequency = models.BigIntegerField(null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            if self.at_frequency:
                return min_typ_max_to_str(self.min, self.typ, self.max, decimal_impedance_to_str) + " @ {}".format(decimal_frequency_to_str(self.at_frequency))
            else:
                return min_typ_max_to_str(self.min, self.typ, self.max, decimal_impedance_to_str)
