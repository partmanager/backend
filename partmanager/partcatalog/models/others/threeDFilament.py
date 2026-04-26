from django.db import models

from partcatalog.models.product import Product
from partcatalog.models.choices import PART_TYPE


class FilamentTypes(models.IntegerChoices):
    ABS = 1
    PETG = 2
    PLA = 3
    TPU = 4


    @staticmethod
    def from_string(type_str):
        values = {
            'ABS': 1,
            'PETG': 2,
            'PLA': 3,
            'TPU': 4,

        }
        if type_str in values:
            return values[type_str]
        else:
            raise ValueError(f"Invalid Filament Type: {type_str}")


class Filament(Product):
    part_type_subset = list(dict(dict(PART_TYPE)['3DFilament']).keys())
    material = models.IntegerField(choices=FilamentTypes.choices)
    color = models.CharField(max_length=30)
    weight = models.FloatField()

    def generate_description(self):
        description = f"3D Filament {self.material}, {self.color}"
        return description

    class Meta:
        ordering = ['material', 'color', 'weight']

    def process_generic(self):
        if self.generic:
            if self.filters:
                pass
            else:
                pass

    def __str__(self):
        return '{} {}'.format(self.manufacturer.name, self.MPN)
