from .part import Part
from django.db import models
from .fields.backlight import Backlight
from .fields.controller import Controller
from .fields.resolution import Resolution


class Display(Part):
    part_type_subset = ['DIS']
    color = models.CharField(max_length=100, null=True, blank=True)
    resolution = Resolution()
    controller = Controller()
    backlight = Backlight()

    def generate_description(self):
        return "{}, {}x{}, {}".format(self.get_part_type_display(), self.resolution.width, self.resolution.height, self.controller.part_number)