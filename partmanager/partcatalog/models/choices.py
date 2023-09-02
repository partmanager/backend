from django.db import models


class BatteryType(models.IntegerChoices):
    CR2030 = 1
    CR2032 = 2
    R6 = 3

    @staticmethod
    def from_string(type_str):
        values = {'CR2030': 1, "CR2032": 2, 'R6': 3, 'AA, R6': 3}
        return values[type_str]


class BatteryClassification(models.IntegerChoices):
    ALKALINE = 1

    @staticmethod
    def from_string(type_str):
        values = {'Alkaline': 1}
        return values[type_str]


class MaterialType(models.IntegerChoices):
    SOLDER_PASTE = 1

    @staticmethod
    def from_string(type_str):
        values = {'Solder Paste': 1}
        return values[type_str]


class MSLevel(models.IntegerChoices):
    MSL_1 = 1

    @staticmethod
    def from_string(type_str):
        values = {'MSL 1': 1, 'Level 1': 1, 'Level 1 → J-STD-020': 1}
        return values[type_str]


class ToleranceType(models.IntegerChoices):
    RELATIVE = 1
    ABSOLUTE = 2
    RELATIVE_PPM = 3

    @staticmethod
    def from_string(type_str):
        values = {'relative': 1, 'absolute': 2, 'ppm': 3}
        return values[type_str]
