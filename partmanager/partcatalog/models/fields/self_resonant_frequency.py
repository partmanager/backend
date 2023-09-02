from django.db import models
from composite_field import CompositeField


class SelfResonantFrequency(CompositeField):
    min = models.BigIntegerField(null=True, blank=True)
    typ = models.BigIntegerField(null=True, blank=True)
    max = models.BigIntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None