from django.db import models
from .part import Part
from .fields.current import CurrentAtTemp
from .fields.insulation_resistance import InsulationResistance
from .fields.power import Power
from .fields.resistance import Resistance
from .fields.voltage import Voltage
from .fields.max_voltage import MaxVoltageAtTemp


class Relay(Part):
    class ConfigurationChoices(models.IntegerChoices):
        SPST_NO = 1
        SPDT = 2

        @staticmethod
        def from_string(type_str):
            values = {"SPST-NO": 1, 'SPDT': 2}
            return values[type_str]

    part_type_subset = ['RLY']
    # coil data
    coil_voltage = Voltage()
    coil_must_release_voltage = MaxVoltageAtTemp()
    coil_resistance = Resistance()
    coil_power = Power()
    # contact data
    configuration = models.IntegerField(choices=ConfigurationChoices.choices, null=True, blank=True)
    switching_voltage = Voltage()
    switching_current = CurrentAtTemp()
    contact_resistance = Resistance()
    operating_life = models.IntegerField(null=True, blank=True)

    insulation_resistance = InsulationResistance()

    def generate_description(self):
        description = "Relay {}, {}".format(self.coil_voltage, self.get_configuration_display())
        if self.switching_voltage:
            description = description + ", " + str(self.switching_voltage)
        if self.switching_current:
            description = description + ", " + str(self.switching_current)
        return description
