from django.db import models
from composite_field import CompositeField


class MeltingIntegral(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=6, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=6, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=6, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None