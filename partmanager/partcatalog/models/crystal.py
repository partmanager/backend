from .part import Part
from django.db import models
from .fields.capacitance import Capacitance
from .fields.ageing import Ageing
from .fields.frequency import Frequency
from .fields.frequency_stability import FrequencyStability
from .fields.insulation_resistance import InsulationResistance
from .fields.power import Power
from .fields.resistance import Resistance


class Crystal(Part):
    VIBRATION_MODE = (
        ('F', 'Fundamental'),
        ('TO', 'Third Overton'),
        ('FO', 'Fifth Overton'),
        ('SO', 'Seventh Overton'),
        ('AC', 'AT-Cut'),
        ('UN', 'Unknown')
    )
    part_type_subset = ['COS']
    # absolute maximum ratings
    frequency = Frequency()
    frequency_stability_over_operating_temperature_range = FrequencyStability()
    vibration_mode = models.CharField(max_length=2, choices=VIBRATION_MODE, default='UN')
    # electrical characteristics
    load_capacitance = Capacitance()  #
    shunt_capacitance = Capacitance()  #
    esr = Resistance()  #
    drive_level = Power()  #
    ageing = Ageing()
    insulation_resistance = InsulationResistance()

    def generate_description(self):
        return "{}, {}".format(self.get_part_type_display(), self.frequency.get_typ_display())

    def set_vibration_mode_from_str(self, vibration_mode_from_str):
        vibration_mode = {'Fundamental': 'F', 'Third Overtone': 'TO', 'Fifth Overtone': 'FO', 'Seventh Overtone': 'SO',
                          'AT-Cut': 'AC'}
        self.vibration_mode = vibration_mode[vibration_mode_from_str]

    @staticmethod
    def vibration_mode_from_str(string):
        vibration_mode = {'Fundamental': 'F', 'Third Overtone': 'TO', 'Fifth Overtone': 'FO', 'Seventh Overtone': 'SO',
                          'AT-Cut': 'AC'}
        return vibration_mode[string]

    def __str__(self):
        return "{}, {}".format(self.manufacturer_part_number, self.description)
