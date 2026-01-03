from django.db import models

from .part import Part
from .choices import PART_TYPE
from .fields.max_power import MaxPower
from .fields.resistance import Resistance
from .fields.temperature_coefficient import TemperatureCoefficient
from .fields.max_voltage import MaxVoltage


class Resistor(Part):
    part_type_subset = list(dict(dict(PART_TYPE)['Resistors']).keys())
    resistance = Resistance()
    power = MaxPower()
    power_derating_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_coefficient = TemperatureCoefficient()  # ppm/K
    working_voltage = MaxVoltage()
    overload_voltage = MaxVoltage()
    dielectric_withstanding_voltage = MaxVoltage()
    fields = {**Part.fields_begin,
              'Resistance': 'resistance', 'Power': 'power', 'Tolerance': 'tolerance',
              **Part.fields_end}

    def get_power_display(self):
        return str(self.power)

    def generate_description(self):
        temperature_coefficient = str(self.temperature_coefficient)
        if temperature_coefficient:
            return "Resistor {}, {}, {}".format(self.resistance, self.power, temperature_coefficient)
        else:
            return "Resistor {}, {}".format(self.resistance, self.power)

    @staticmethod
    def resistor_type_from_str(resistor_type_str):
        types = {'Thick Film': 'TKF', 'Thin Film': 'TKN', 'Unknown': 'UNK'}
        return types[resistor_type_str]

    @staticmethod
    def tolerance_type_from_str(resistor_type_str):
        types = {'Relative': '%', 'Absolute': 'r'}
        return types[resistor_type_str]

    class Meta:
        ordering = ['resistance_typ', 'resistance_tolerance_type', 'resistance_relative_tolerance', 'power_max']

    def process_generic(self):
        if self.generic:
            if self.filters:
                pass
            else:
                pass

    def __str__(self):
        return '{} {}'.format(self.manufacturer.name, self.MPN)
