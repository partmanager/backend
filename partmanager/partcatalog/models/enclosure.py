from django.db import models
from .part import Part
from .fields.dimension import Dimension


class Enclosure(Part):
    class Material(models.IntegerChoices):
        UNKNOWN = 0
        ABS = 1

        @staticmethod
        def from_string(type_str):
            values = {"ABS": 1}
            return values[type_str]

    class Color(models.IntegerChoices):
        UNKNOWN = 0
        GRAY = 1
        WHITE = 2

        @staticmethod
        def from_string(type_str):
            values = {"Gray": 1, "White": 2}
            return values[type_str]

    class IPRating(models.IntegerChoices):
        UNKNOWN = 0
        IP30 = 1

        @staticmethod
        def from_string(type_str):
            if len(type_str):
                values = {"IP30": 1}
                return values[type_str]
            else:
                return 0

    class FlameRating(models.IntegerChoices):
        UNKNOWN = 0
        UL94_HB = 1

        @staticmethod
        def from_string(type_str):
            if len(type_str):
                values = {"UL94 HB": 1}
                return values[type_str]
            else:
                return 0

    part_type_subset = ['E', 'EA']
    material = models.IntegerField(choices=Material.choices, default=0)
    color = models.IntegerField(choices=Color.choices, default=0)
    flame_rating = models.IntegerField(choices=FlameRating.choices, default=0)
    ip_rating = models.IntegerField(choices=IPRating.choices, default=0)
    length = Dimension()
    width = Dimension()
    height = Dimension()
    pcb_length = Dimension()
    pcb_width = Dimension()
