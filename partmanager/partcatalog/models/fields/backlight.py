from django.db import models
from composite_field import CompositeField


class Backlight(CompositeField):
    source = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
