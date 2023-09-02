from .part import Part
from django.db import models
from composite_field import CompositeField
from .fields.dc_saturation_current import DCSaturationCurrent
from .fields.current import CurrentAtTemp
from .fields.q_factor import QFactor
from .fields.self_resonant_frequency import SelfResonantFrequency
from .fields.resistance import ResistanceAtTemp
from .fields.inductance import InductanceAtFrequencyAtTemp
from .fields.voltage import Voltage


class InductanceTolerance(CompositeField):
    TYPE = [
        ('%', 'RELATIVE'),
        ('uH', 'ABSOLUTE')
    ]
    over = models.DecimalField(max_digits=7, decimal_places=5, null=True, blank=True)
    under = models.DecimalField(max_digits=7, decimal_places=5, null=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE, default='%')

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.over is not None or self.under is not None


class Inductor(Part):
    part_type_subset = ['I']
    inductance = InductanceAtFrequencyAtTemp()
    inductance_tolerance = InductanceTolerance()
    dc_resistance = ResistanceAtTemp()
    dc_rated_current = CurrentAtTemp()
    q_factor = QFactor()
    dc_saturation_current_max_values_count = 2
    dc_saturation_current_1 = DCSaturationCurrent()
    dc_saturation_current_2 = DCSaturationCurrent()
    srf = SelfResonantFrequency()
    rated_operating_voltage = Voltage()

    class Meta:
        ordering = ['inductance_typ', 'dc_rated_current_max']

    def generate_description(self):
        return "Inductor, {}".format(self.inductance)

    def __str__(self):
        return self.manufacturer_part_number
