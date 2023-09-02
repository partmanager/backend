from django.db import models
from composite_field import CompositeField
from .min_typ_max_field_to_str import min_typ_max_to_str


class LuminousIntensity(CompositeField):
    min = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    typ = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    max = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def __str__(self):
            min_typ_max_to_str(self.min, self.typ, self.max)
