from django.db import models
from .part import Part
from .fields.capacitance import CapacitanceAtFreq
from .fields.current import CurrentAtTemp
from .fields.decibel import Decibel
from .fields.voltage import Voltage


class ESDSuppressor(Part):
    part_type_subset = ['ESD']
    rated_voltage = Voltage()
    clamping_voltage = Voltage()
    trigger_voltage = Voltage()
    capacitance = CapacitanceAtFreq()
    attenuation = Decibel()
    leakage_current = CurrentAtTemp()
    esd_pulse_withstand_count = models.IntegerField()

    def generate_description(self):
        if self.rated_voltage:
            return "ESD Suppressor, Vr={}".format(self.rated_voltage)
        return "ESD Suppressor, Vc={}".format(self.clamping_voltage)
