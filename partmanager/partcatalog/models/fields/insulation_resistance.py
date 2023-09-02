from django.db import models
from composite_field import CompositeField


class InsulationResistance(CompositeField):
    min = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    typ = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    max = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    at_voltage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def get_min_display(self):
            return decimal_resistance_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_resistance_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_resistance_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            if self.at_voltage:
                return "{}".format(decimal_voltage_to_str(self.at_voltage))
            else:
                return ''
