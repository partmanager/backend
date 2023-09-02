from django.db import models
from composite_field import CompositeField


class ClampingVoltage(CompositeField):
    max = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in volts
    at_peak_current = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in ampere