from django.db import models
from composite_field import CompositeField


class ThermalResistance(CompositeField):
    min = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None