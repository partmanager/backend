from django.db import models
from .common import Package
from .fields import Dimension


class SOPackage(Package):
    dimensions_names = ['A', 'A1', 'b', 'c', 'D', 'e', 'E', 'E1', 'L']
    pin_count = models.PositiveIntegerField(default=0)
    A = Dimension()
    A1 = Dimension()
    b = Dimension()
    c = Dimension()
    D = Dimension()
    e = Dimension()
    E = Dimension()
    E1 = Dimension()
    L = Dimension()

    @property
    def dimensions(self):
        dimensions = []
        for dim_str in self.dimensions_names:
            dimensions.append(
                {
                    'symbol': dim_str,
                    #'name': '',
                    **getattr(self, dim_str).to_string_dict()
                }
            )
        return dimensions