from django.db import models
from .part import Part


class GenericPart(Part):
    parts = models.ManyToManyField(Part)
    filters = models.JSONField()