from django.db import models
from .part import Part
from .fields.dimension import Dimension


class Lightpipe(Part):
    class ShapeType(models.IntegerChoices):
        ROUND = 1

        @staticmethod
        def from_string(type_str):
            values = {'Round': 1}
            return values[type_str]

    class Color(models.IntegerChoices):
        TRANSPARENT = 1

        @staticmethod
        def from_string(type_str):
            values = {'Transparent': 1}
            return values[type_str]

    part_type_subset = ['LPI']
    shape = models.IntegerField(choices=ShapeType.choices)
    color = models.IntegerField(choices=Color.choices)
    light_count = models.IntegerField()
    length = Dimension()
    panel_cutout_diameter = Dimension()
