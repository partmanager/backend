from django.db import models


class BatteryType(models.IntegerChoices):
    CR2030 = 1
    CR2032 = 2
    R6 = 3
    CR14250 = 4

    @staticmethod
    def from_string(type_str):
        values = {'CR2030': 1, "CR2032": 2, 'R6': 3, 'AA, R6': 3, 'CR14250': 4}
        return values[type_str]


class BatteryClassification(models.IntegerChoices):
    ALKALINE = 1
    LITHIUM = 2

    @staticmethod
    def from_string(type_str):
        values = {'Alkaline': 1, 'Lithium': 2}
        return values[type_str]


class MaterialType(models.IntegerChoices):
    SOLDER_PASTE = 1

    @staticmethod
    def from_string(type_str):
        values = {'Solder Paste': 1}
        return values[type_str]


class MSLevel(models.IntegerChoices):
    MSL_1 = 1
    MSL_2 = 2
    MSL_2a = 22
    MSL_3 = 3
    MSL_4 = 4
    MSL_5 = 5
    MSL_5a = 52
    MSL_6 = 6

    @staticmethod
    def from_string(type_str):
        values = {'MSL-1 UNLIM': 1,
                  'MSL-2 1-YEAR': 2,
                  'MSL-2A 4-WEEKS': 22,
                  'MSL-3 168-HOURS': 3,
                  'MSL-4 72-HOURS': 4,
                  'MSL-5 48-HOURS': 5,
                  'MSL-5A 24-HOURS': 52,
                  'MSL-6 TOL': 6}
        if type_str in values:
            return values[type_str]
        else:
            raise ValueError(f"Invalid MSL level: {type_str}")


class ToleranceType(models.IntegerChoices):
    RELATIVE = 1
    ABSOLUTE = 2
    RELATIVE_PPM = 3

    @staticmethod
    def from_string(type_str):
        values = {'relative': 1, 'absolute': 2, 'ppm': 3}
        return values[type_str]
