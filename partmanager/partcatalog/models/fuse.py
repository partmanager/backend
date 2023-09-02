from django.db import models
from .part import Part
from .fields.max_current import MaxCurrentAtTemp
from .fields.melting_integral import MeltingIntegral
from .fields.max_voltage import MaxVoltageAtTemp


class Fuse(Part):
    # class Technology(models.IntegerChoices):
    #     LTCC = 1  # multilayer
    #
    #     @staticmethod
    #     def from_string(type_str):
    #         values = {"LTCC": 1}
    #         return values[type_str]

    part_type_subset = ['FUS']
    #technology = models.IntegerField(choices=Technology.choices)
    rated_current = MaxCurrentAtTemp()
    rated_voltage = MaxVoltageAtTemp()
    breaking_capacity = MaxCurrentAtTemp()
    voltage_drop = MaxVoltageAtTemp()
    melting_integral = MeltingIntegral()

    def generate_description(self):
        return "Fuse, {}, {}".format(self.rated_current, self.rated_voltage)

