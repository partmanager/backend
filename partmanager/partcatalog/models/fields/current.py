from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str
from .si_unit_to_string import decimal_current_to_str


class Current(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_current_to_str)


class CurrentAtTemp(CompositeField):
    min = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_current_to_str)
