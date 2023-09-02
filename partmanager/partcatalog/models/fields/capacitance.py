from django.db import models
from composite_field import CompositeField
from ..to_string_conversions import decimal_capacitance_to_str, decimal_frequency_to_str
from ..choices import ToleranceType
from .min_typ_max_field_to_str import min_typ_max_to_str


class Capacitance(CompositeField):
    min = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    typ = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    max = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    relative_tolerance = models.FloatField(null=True, blank=True)  # field mainly used for ordering
    tolerance_type = models.IntegerField(choices=ToleranceType.choices, default=ToleranceType.RELATIVE)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_capacitance_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_capacitance_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_capacitance_to_str(self.max) if self.max else ''

        def get_capacitance_display(self):
            return _get_capacitance_display(self.min, self.typ, self.max)

        def get_tolerance_display(self):
            return _get_tolerance_display(self.min, self.typ, self.max, self.tolerance_type)

        def get_condition_display(self):
            return ""

        def __str__(self):
            tolerance_str = self.get_tolerance_display()
            if tolerance_str:
                return "{} {}".format(self.get_capacitance_display(), tolerance_str)
            else:
                return self.get_capacitance_display()


class CapacitanceAtFreq(CompositeField):
    min = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    typ = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    max = models.DecimalField(max_digits=14, decimal_places=14, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=16, decimal_places=3, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def __str__(self):
            value = min_typ_max_to_str(self.min, self.typ, self.max, decimal_capacitance_to_str)
            if self.at_frequency:
                value = value + " @ " + decimal_frequency_to_str(self.at_frequency)
            return value

        def get_min_display(self):
            return decimal_capacitance_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_capacitance_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_capacitance_to_str(self.max) if self.max else ''

        def get_capacitance_display(self):
            return _get_capacitance_display(self.min, self.typ, self.max)

        def get_tolerance_display(self):
            return _get_tolerance_display(self.min, self.typ, self.max, self.tolerance_type)

        def get_condition_display(self):
            return ""


def _get_capacitance_display(min, typ, max):
    if typ is not None:
        return decimal_capacitance_to_str(typ)
    elif min is not None:
        return "min. " + decimal_capacitance_to_str(min)
    elif max is not None:
        return "max. " + decimal_capacitance_to_str(max)


def _get_tolerance_display(min, typ, max, tolerance_type):
    if tolerance_type == ToleranceType.RELATIVE:
        if min is not None and max is not None:
            over = (max - typ) / typ * 100
            under = (min - typ) / typ * 100
            if abs(under) == abs(over):
                return "±{}%".format(str(abs(under)).rstrip('0').rstrip('.'))
            else:
                return "{}/{}%".format(str(under).rstrip('0').rstrip('.'),
                                       str(over).rstrip('0').rstrip('.'))
        elif min is not None:
            return "{}%".format(str(min).rstrip('0').rstrip('.'))
        elif max is not None:
            return "{}%".format(str(max).rstrip('0').rstrip('.'))
    else:
        if min is not None and max is not None:
            over = max - typ
            under = min - typ
            if abs(under) == abs(over):
                return "±{}".format(decimal_capacitance_to_str(abs(under)))
            else:
                return "{}/{}".format(decimal_capacitance_to_str(under),
                                      decimal_capacitance_to_str(over))
        elif min is not None:
            return "{}".format(decimal_capacitance_to_str(min))
        elif max is not None:
            return "{}".format(decimal_capacitance_to_str(max))
