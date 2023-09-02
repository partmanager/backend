from .part import Part
from django.db import models


class Connector(Part):
    BUS_TYPE = [
        ('M.2_E', 'M.2 Key E'),
        ('M.2_B', 'M.2 Key B'),
        ('M.2', 'M.2'),
        ('SIM', 'SIM'),
        ('ETH', 'Ethernet'),
        ('mPCIe', 'Mini PCI-E')
    ]

    class ContactPositionChoices(models.IntegerChoices):
        TOP = 1
        BOTTOM = 2

        @staticmethod
        def from_string(type_str):
            values = {"Top": 1, "Bottom": 2}
            return values[type_str]

    part_type_subset = list(dict(dict(Part.PART_TYPE)['Connectors']).keys())
    contact_position = models.IntegerField(choices=ContactPositionChoices.choices, null=True, blank=True)
    bus_type = models.CharField(max_length=5, choices=BUS_TYPE, null=True, blank=True)
    pin_count = models.IntegerField(null=True, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    pin_spacing = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    row_spacing = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pin_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pin_height_form_pcb = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    housing_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    @staticmethod
    def bus_from_str(bus_str):
        if bus_str:
            values = {'M.2 Key E': 'M.2_E', 'M.2 Key B': 'M.2_B', 'M.2': 'M.2', 'SIM Card': 'SIM', 'Ethernet': 'ETH',
                      'Mini PCI-E': 'mPCIe'}
            return values[bus_str]

    def generate_description(self):
        if self.part_type != 'COB':
            if self.pin_count and self.row_count:
                pin_per_row = int(self.pin_count) / int(self.row_count)
                return f"{self.get_part_type_display()}, {self.pin_count} pin, {self.row_count}x{pin_per_row}, {self.pin_spacing}"
            elif self.pin_count:
                return f"{self.get_part_type_display()}, {self.pin_count} pin, {self.pin_spacing}"
        return ''