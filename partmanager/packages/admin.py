from django.contrib import admin

from .models.ChipCapacitorPackage import ChipCapacitorPackage
from .models.ChipResistorPackage import ChipResistorPackage


# Register your models here.
admin.site.register(ChipCapacitorPackage)
admin.site.register(ChipResistorPackage)
