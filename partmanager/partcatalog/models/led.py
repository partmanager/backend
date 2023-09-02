from django.db import models
from .part import Part
from .fields.current import Current
from .fields.forward_voltage import ForwardVoltage
from .fields.luminous_intensity import LuminousIntensity
from .fields.max_voltage import MaxVoltageAtTemp


class LED(Part):
    COLOR = [
        ('B', 'Blue'),
        ('G', 'Green'),
        ('R', 'Red')
    ]
    part_type_subset = ['DLE']
    continuous_forward_current = Current()
    peak_forward_current = Current()
    forward_voltage = ForwardVoltage()
    luminous_intensity = LuminousIntensity()
    viewing_angle_in_deg = models.IntegerField(null=True, blank=True)
    reverse_voltage = MaxVoltageAtTemp()
    color = models.CharField(max_length=3, choices=COLOR)

    def generate_description(self):
        return "LED " + self.get_color_display()

    @staticmethod
    def color_from_str(color_str):
        values = {'Blue': 'B', 'Green': 'G', 'Red': 'R', 'Yellow': 'Y'}
        return values[color_str]
