from .part import Part
from .fields.resistance import ResistanceAtTemp
from .fields.battery_capacity import BatteryCapacity
from .fields.voltage import Voltage
from .choices import BatteryType, BatteryClassification
from django.db import models


class Battery(Part):
    part_type_subset = ['BAT']
    battery_type = models.IntegerField(choices=BatteryType.choices)
    classification = models.IntegerField(choices=BatteryClassification.choices)
    nominal_voltage = Voltage() # todo change to voltage at temp
    internal_resistance = ResistanceAtTemp()
    capacity_max_values_count = 4
    capacity_1 = BatteryCapacity()
    capacity_2 = BatteryCapacity()
    capacity_3 = BatteryCapacity()
    capacity_4 = BatteryCapacity()

    def generate_description(self):
        return "Battery, {} {}".format(self.get_battery_type_display(), self.get_classification_display())
