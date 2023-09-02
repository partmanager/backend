import math
from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_degree_to_str, decimal_rad_to_str


class Phase(CompositeField):
    """
    Phase data is stored as radians, you can use phase_from_degree(..) or phase_from_radian(..)
    """
    min = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    typ = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    max = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.min is not None or self.max is not None

        def __to_string(self, value, as_deg):
            if as_deg:
                return decimal_degree_to_str(math.degrees(value))
            else:
                return decimal_rad_to_str(value)

        def get_min_display(self, as_deg=False):
            return self.__to_string(self.min, as_deg) if self.min else ''

        def get_typ_display(self, as_deg=False):
            return self.__to_string(self.typ, as_deg) if self.typ else ''

        def get_max_display(self, as_deg=False):
            return self.__to_string(self.max, as_deg) if self.max else ''


def phase_from_degree(minimum, typ, maximum):
    phase = Phase()
    phase.min = math.radians(minimum)
    phase.typ = math.radians(typ)
    phase.max = math.radians(maximum)
    return phase


def phase_from_radian(minimum, typ, maximum):
    phase = Phase()
    phase.min = minimum
    phase.typ = typ
    phase.max = maximum
    return phase