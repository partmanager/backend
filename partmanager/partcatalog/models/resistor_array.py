from .part import Part
from django.db import models
from .fields.max_power import MaxPower
from .fields.resistance import Resistance
from .fields.max_voltage import MaxVoltage


class ResistorArray(Part):
    elements_count = models.IntegerField()
    resistance = Resistance()
    power_rating_per_resistor = MaxPower()
    power_rating_package = MaxPower()
    working_voltage = MaxVoltage()
    overload_voltage = MaxVoltage()

    def generate_description(self):
        description = "Resistor Array {} elements, {}".format(self.elements_count, str(self.resistance))
        if self.power_rating_package:
            description = description + ", " + str(self.power_rating_package)
        if self.working_voltage:
            description = description + ", " + str(self.working_voltage)
        return description
