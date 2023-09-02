from django.contrib import admin

# Register your models here.
from .models.balun import Balun
from .models.battery import Battery
from .models.battery_holder import BatteryHolder
from .models.bridge_rectifier import BridgeRectifier
from .models.files import File, FileVersion
from .models.fuse import Fuse
from .models.integrated_circuit import IntegratedCircuit
from .models.resistor import Resistor
from .models.surge_arrester import SurgeArrester
from .models.manufacturer_order_number import ManufacturerOrderNumber
from .models.capacitor import Capacitor
from .models.connector import Connector
from .models.crystal import Crystal
from .models.crystal_oscillator import CrystalOscillator
from .models.diode import Diode, TVS
from .models.esd_suppressor import ESDSuppressor
from .models.led import LED
from .models.lightpipe import Lightpipe
from .models.inductor import Inductor
from .models.ptc_fuse import PTCFuse
from .models.relay import Relay
from .models.transistor_bipolar import TransistorBipolar
from .models.transistor_mosfet import TransistorMosfet
from .models.ferrite_bead import FerriteBead


admin.site.register(File)
admin.site.register(FileVersion)

admin.site.register(ManufacturerOrderNumber)

admin.site.register(Balun)
admin.site.register(Battery)
admin.site.register(BatteryHolder)
admin.site.register(BridgeRectifier)
admin.site.register(Connector)
admin.site.register(Crystal)
admin.site.register(CrystalOscillator)
admin.site.register(Diode)
admin.site.register(ESDSuppressor)
admin.site.register(FerriteBead)
admin.site.register(Fuse)
admin.site.register(LED)
admin.site.register(Lightpipe)
admin.site.register(TVS)
admin.site.register(Inductor)
admin.site.register(PTCFuse)
admin.site.register(Relay)
admin.site.register(Resistor)
admin.site.register(SurgeArrester)
admin.site.register(IntegratedCircuit)
admin.site.register(TransistorBipolar)
admin.site.register(TransistorMosfet)


@admin.register(Capacitor)
class CapacitorAdmin(admin.ModelAdmin):
    list_display = ('manufacturer_part_number', 'capacitance', 'voltage', 'manufacturer')
