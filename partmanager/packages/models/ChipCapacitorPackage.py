from .common import ChipPackageBase, inch_to_mm
from .fields import Dimension


class ChipCapacitorPackage(ChipPackageBase):
    """ name field is representing case code in inches """

    e = Dimension()  # Terminal size in mm
    g = Dimension()  # Terminal size in mm

    @property
    def dimensions(self):
        return [{'name': 'Length', 'symbol': 'L', **self.length.to_string_dict()},
                {'name': 'Width', 'symbol': 'W', **self.width.to_string_dict()},
                {'name': 'Thickness', 'symbol': 'H', **self.thickness.to_string_dict()},
                {'name': 'Terminal length', 'symbol': 'e', **self.e.to_string_dict()}
                ]

    @property
    def case_code_metric(self):
        return inch_to_mm[self.name]

    @property
    def case_code_imperial(self):
        return self.name

    @staticmethod
    def generate_description(name, dimensions):
        return 'Chip Capacitor ' + name + '(' + inch_to_mm[name] + ')'

    @classmethod
    def create(cls, name, dimensions):
        package = cls(type='Chip Capacitor', name=name,
                      description=ChipCapacitorPackage.generate_description(name, dimensions),
                      **dimensions)
        return package

    def __str__(self):
        return 'Chip Capacitor ' + str(self.name) + '(' + inch_to_mm[self.name] + ')'