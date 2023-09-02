from .common import ChipPackageBase, inch_to_mm
from .fields import Dimension


class ChipResistorPackage(ChipPackageBase):
    t1 = Dimension()  # Terminal size on top
    t2 = Dimension()  # Terminal size on bottom

    @staticmethod
    def generate_description(name, dimensions):
        return 'Chip Resistor ' + name + '(' + inch_to_mm[name] + ')'

    @classmethod
    def create(cls, name, dimensions):
        package = cls(type='Chip Resistor', name=name,
                      description=ChipResistorPackage.generate_description(name, dimensions),
                      **dimensions)
        return package

    @property
    def dimensions_drawing(self):
        return '/package_dimension_drawing/chip_resistor_package_dimensions.svg'

    @property
    def dimensions(self):
        return [{'name': 'Length', 'symbol': 'L', **self.length.to_string_dict()},
                {'name': 'Width', 'symbol': 'W', **self.width.to_string_dict()},
                {'name': 'Thickness', 'symbol': 'H', **self.thickness.to_string_dict()},
                {'name': 'Terminal length top', 'symbol': 'T1', **self.t1.to_string_dict()},
                {'name': 'Terminal length bottom', 'symbol': 'T2', **self.t2.to_string_dict()}
                ]

    def to_ajax(self):
        response = super(ChipPackageBase, self).to_ajax()
        response['files']['dimensions_drawing'] = self.hostname + '/static' + self.dimensions_drawing
        response['dimensions'] = self.dimensions
        return response
