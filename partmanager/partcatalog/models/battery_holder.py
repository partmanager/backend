from .part import Part
from .choices import BatteryType
from django.db import models


class BatteryHolder(Part):
    part_type_subset = ['BH']
    battery_type = models.IntegerField(choices=BatteryType.choices)
    battery_count = models.IntegerField()

    def generate_description(self):
        return "Battery Holder, {} x {}".format(self.battery_count, self.get_battery_type_display())
