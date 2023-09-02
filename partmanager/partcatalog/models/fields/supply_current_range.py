from django.db import models
from composite_field import CompositeField


class SupplyCurrentRange(CompositeField):
    min = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None