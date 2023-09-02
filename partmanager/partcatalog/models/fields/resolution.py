from django.db import models
from composite_field import CompositeField


class Resolution(CompositeField):
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
