from composite_field import CompositeField
from django.db import models


class Dimension(CompositeField):
    value = models.DecimalField(max_digits=6, decimal_places=3)  # in mm
    tolerance_oversize = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)  # in mm
    tolerance_undersize = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)  # in mm

    class Proxy(CompositeField.Proxy):
        def to_string_dict(self):
            def tolerance_to_str():
                if self.tolerance_oversize and self.tolerance_undersize:
                    if abs(self.tolerance_oversize) == abs(self.tolerance_undersize):
                        return '±{} mm'.format(abs(self.tolerance_oversize))
                    else:
                        return '{}/{} mm'.format(self.tolerance_oversize, self.tolerance_undersize)
                elif self.tolerance_oversize:
                    return '{} mm'.format(self.tolerance_oversize)
                elif self.tolerance_undersize:
                    return '{} mm'.format(self.tolerance_undersize)

            return {'value': '{} mm {}'.format(self.value, tolerance_to_str()) if tolerance_to_str() else '{} mm'.format(self.value),
                    'max': '{} mm'.format(self.value + self.tolerance_oversize) if self.tolerance_oversize else '-',
                    'min': '{} mm'.format(self.value + self.tolerance_undersize) if self.tolerance_undersize else '-'}

        def to_dict(self):
            return {'value': self.value,
                    'tol_over': self.tolerance_oversize,
                    'tol_under': self.tolerance_undersize}