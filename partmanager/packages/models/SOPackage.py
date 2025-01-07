from django.db import models
from .common import Package
from .fields import Dimension
from part_library_gen.packages.dimension import Dimension as PartLibraryDimension
from part_library_gen.packages.tssop import TSSOP


def converDimension(dimension):
    return PartLibraryDimension(
        min_=dimension.tolerance_undersize,
        max_=dimension.tolerance_oversize,
        typ=dimension.value
    )

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

    def to_part_lib_gen_obj(self):
        return TSSOP(
            pin_count=self.pin_count,
            A=converDimension(self.A),
            A1=converDimension(self.A1),
            b=converDimension(self.b),
            c=converDimension(self.c),
            D=converDimension(self.D),
            e=converDimension(self.e),
            E=converDimension(self.E),
            E1=converDimension(self.E1),
            L=converDimension(self.L)
        )