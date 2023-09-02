from django.db import models
from composite_field import CompositeField
from ..choices import ToleranceType
from ..to_string_conversions import decimal_resistance_to_str
from .min_typ_max_field_to_str import min_typ_max_to_str


class Resistance(CompositeField):
    min = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    typ = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    max = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    relative_tolerance = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True) #  field mainly used for ordering
    tolerance_type = models.IntegerField(choices=ToleranceType.choices, default=ToleranceType.RELATIVE)

    class Proxy(CompositeField.Proxy):
        def get_resistance_display(self):
            return _get_resistance_display(self.min, self.typ, self.max)

        def get_tolerance_display(self):
            return _get_tolerance_display(self.min, self.typ, self.max, self.tolerance_type)

        def __bool__(self):
            return self.min is not None or self.typ is not None or self.max is not None

        def __str__(self):
            tolerance_str = self.get_tolerance_display()
            if tolerance_str:
                return "{} {}".format(self.get_resistance_display(), tolerance_str)
            else:
                return self.get_resistance_display()


class ResistanceAtTemp(CompositeField):
    min = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    typ = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    max = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    relative_tolerance = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True) #  field mainly used for ordering
    tolerance_type = models.IntegerField(choices=ToleranceType.choices, default=ToleranceType.RELATIVE)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def get_resistance_display(self):
            return min_typ_max_to_str(self.min, self.typ, self.max, decimal_resistance_to_str)
            #return _get_resistance_display(self.min, self.typ, self.max)

        def get_tolerance_display(self):
            return _get_tolerance_display(self.min, self.typ, self.max, self.tolerance_type)

        def __bool__(self):
            return self.min is not None or self.typ is not None or self.max is not None

        def __str__(self):
            values = 0
            if self.min:
                values += 1
            if self.typ:
                values += 1
            if self.max:
                values += 1
            if values >= 2:
                return "{} {}".format(self.get_resistance_display(), self.get_tolerance_display())
            else:
                return self.get_resistance_display()


def _get_resistance_display(min, typ, max):
    if typ is not None:
        return decimal_resistance_to_str(typ)
    else:
        "Unimplemented"


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
                return "±{}".format(str(abs(under)).rstrip('0').rstrip('.'))
            else:
                return "{}/{}".format(str(under).rstrip('0').rstrip('.'),
                                      str(over).rstrip('0').rstrip('.'))
        elif min is not None:
            return "{}".format(str(min).rstrip('0').rstrip('.'))
        elif max is not None:
            return "{}".format(str(max).rstrip('0').rstrip('.'))


