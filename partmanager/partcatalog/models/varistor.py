from django.db import models

from .part import Part

from .fields.clamping_voltage import ClampingVoltage
from .fields.voltage import Voltage


class Varistor(Part):
    voltage = Voltage()
    rated_rms_voltage = Voltage()
    rated_dc_voltage = Voltage()
    clamping_voltage = ClampingVoltage()
    power_rating = models.FloatField(null=True, blank=True)  # in [W]

    def generate_description(self):
        if self.power_rating:
            return f"Varistor, {self.voltage} {self.power_rating: .2f}W"
        else:
            return f"Varistor, {self.voltage}"
