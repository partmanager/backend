from django.db import models
from composite_field import CompositeField


class Controller(CompositeField):
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    part_number = models.CharField(max_length=100, null=True, blank=True)
    interface = models.CharField(max_length=100, null=True, blank=True)
