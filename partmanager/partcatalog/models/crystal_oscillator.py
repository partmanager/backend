from django.db import models
from .part import Part
from .fields.supply_current_range import SupplyCurrentRange
from .fields.supply_voltage_range import SupplyVoltageRange
from .fields.ageing import Ageing
from .fields.frequency import Frequency
from .fields.frequency_stability import FrequencyStability
from .fields.rise_time import RiseTime
from .fields.fall_time import FallTime
from .fields.time import Time


class CrystalOscillator(Part):
    part_type_subset = ['CRO']
    frequency = Frequency()
    supply_voltage = SupplyVoltageRange()
    supply_current = SupplyCurrentRange()
    standby_current = SupplyCurrentRange()
    frequency_stability_over_operating_temperature_range = FrequencyStability()
    rise_time = RiseTime()
    fall_time = FallTime()
    startup_time = Time()
    # output_load
    peak_to_peak_jitter = Time()
    rms_jitter = Time()
    ageing = Ageing()
    enable_pin = models.BooleanField(null=True, blank=True)
    tri_state_output = models.BooleanField(null=True, blank=True)

    def generate_description(self):
        return "{}, {}".format(self.get_part_type_display(), self.frequency)
