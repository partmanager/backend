from .part import Part
from django.db import models
from .fields.insulation_resistance import InsulationResistance
from .fields.current import CurrentAtTemp
from .fields.resistance import ResistanceAtTemp
from .fields.dimension import Dimension
from .fields.max_voltage import MaxVoltage


class Switch(Part):
    class SwitchType(models.IntegerChoices):
        DIP = 1
        TACT_SWITCH = 2
        ENCODING_SWITCH = 3

        @staticmethod
        def from_string(type_str):
            values = {"DIP Switch": 1,
                      "Tact Switch": 2,
                      "Encoding Switch": 3}
            return values[type_str]

    class ConfigurationChoices(models.IntegerChoices):
        SPST_NO = 1

        @staticmethod
        def from_string(type_str):
            values = {"SPST-NO": 1}
            return values[type_str]

    part_type_subset = ['S']
    switch_type = models.IntegerField(choices=SwitchType.choices)
    configuration = models.IntegerField(choices=ConfigurationChoices.choices, null=True, blank=True)
    position_count = models.IntegerField()
    pin_pitch = Dimension()
    switching_voltage = MaxVoltage()
    switching_current = CurrentAtTemp()
    contact_resistance = ResistanceAtTemp()
    insulation_resistance = InsulationResistance()
    # dielectric_strength
    operating_life = models.IntegerField(null=True, blank=True)

    def generate_description(self):
        description = "{}, pos={}".format(self.get_switch_type_display(), self.position_count)
        if self.switching_current:
            description = description + ", " + str(self.switching_current)
        if self.switching_voltage:
            description = description + ", " + str(self.switching_voltage)
        return description
