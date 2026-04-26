from django.db import models

class PackageTypes(models.IntegerChoices):
    RESISTOR_CHIP = 1
    CAPACITOR_CHIP = 2
    SO = 3


packages = {
    1: "Resistor Chip",
    2: "Capacitor Chip",
}