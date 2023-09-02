from django.db import models
from .part import Part
from .fields.decibel import Decibel
from .fields.frequency_range import FrequencyRange
from .fields.impedance import ImpedanceAtFreq
from .fields.phase import Phase
from .fields.power import Power
from .fields.return_loss import ReturnLoss


class Balun(Part):
    class Technology(models.IntegerChoices):
        LTCC = 1  # multilayer

        @staticmethod
        def from_string(type_str):
            values = {"LTCC": 1}
            return values[type_str]

    part_type_subset = ['BAL']
    technology = models.IntegerField(choices=Technology.choices)
    operating_frequency_range = FrequencyRange()
    unbalanced_port_impedance = ImpedanceAtFreq()
    balanced_port_impedance = ImpedanceAtFreq()
    unbalanced_port_return_loss = ReturnLoss()
    phase_balance = Phase()
    amplitude_balance = Decibel()
    insertion_loss = Decibel()
    power_rating = Power()  # TODO replace with max_power

    class Meta:
        ordering = ['unbalanced_port_impedance_typ',
                    'balanced_port_impedance_max',
                    'power_rating_max',
                    'unbalanced_port_return_loss_typ']

    def get_unbalanced_port_impedance_display(self):
        return str(self.unbalanced_port_impedance)

    def get_balanced_port_impedance_display(self):
        return str(self.balanced_port_impedance)

    def get_operating_frequency_range_display(self):
        return str(self.operating_frequency_range)

    def get_power_rating_display(self):
        return str(self.power_rating)

    def generate_description(self):
        return "Balun, {}, {}, {} -> {}".format(self.operating_frequency_range, self.power_rating,
                                                self.balanced_port_impedance, self.unbalanced_port_impedance)
