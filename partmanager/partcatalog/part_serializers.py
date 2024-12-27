from rest_framework import serializers

from manufacturers.serializers import ManufacturerSerializer
from symbolandfootprint.serializers import SymbolSerializer
from .serializers import FileSerializer, ManufacturerOrderNumberWithLocationsSerializer

from .models.part import Part
from .models.balun import Balun
from .models.battery import Battery
from .models.battery_holder import BatteryHolder
from .models.bridge_rectifier import BridgeRectifier
from .models.capacitor import Capacitor
from .models.common_mode_choke import CommonModeChoke
from .models.connector import Connector
from .models.crystal import Crystal

from .models.diode import Diode, TVS

from .models.enclosure import Enclosure

from .models.ferrite_bead import FerriteBead

from .models.inductor import Inductor
from .models.integrated_circuit import IntegratedCircuit
from .models.led import LED
from .models.module import Module
from .models.resistor import Resistor
from .models.switch import Switch
from .models.transistor_bipolar import TransistorBipolar
from .models.transistor_mosfet import TransistorMosfet
from rest_polymorphic.serializers import PolymorphicSerializer


common_fields = ['id', 'manufacturer_part_number', 'manufacturer_order_number_set', 'product_url', 'production_status',
                 'operating_conditions', 'storage_conditions', 'package', 'symbol', 'manufacturer', 'description',
                 'notes', 'comment', 'distributors', 'files']


class PartBaseSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    storage_conditions = serializers.SerializerMethodField()
    operating_conditions = serializers.SerializerMethodField()
    files = FileSerializer(many=True, read_only=True)
    manufacturer_order_number_set = ManufacturerOrderNumberWithLocationsSerializer(many=True, read_only=True)
    distributors = serializers.SerializerMethodField()
    symbol = SymbolSerializer()

    class Meta:
        model = Part
        fields = common_fields

    def get_operating_conditions(self, obj):
        return obj.operating_conditions.to_dict()

    def get_storage_conditions(self, obj):
        return obj.storage_conditions.to_ajax()

    def get_distributors(self, obj):
        return obj.distributor_pk_set()


class BalunSerializer(PartBaseSerializer):
    unbalanced_port_impedance = serializers.SerializerMethodField()
    balanced_port_impedance = serializers.SerializerMethodField()
    operating_frequency_range = serializers.SerializerMethodField()
    power_rating = serializers.SerializerMethodField()

    class Meta:
        model = Balun
        fields = common_fields + ['unbalanced_port_impedance', 'balanced_port_impedance', 'operating_frequency_range', 'power_rating']

    def get_unbalanced_port_impedance(self, obj):
        return obj.get_unbalanced_port_impedance_display()

    def get_balanced_port_impedance(self, obj):
        return obj.get_balanced_port_impedance_display()

    def get_operating_frequency_range(self, obj):
        return obj.get_operating_frequency_range_display()

    def get_power_rating(self, obj):
        return obj.get_power_rating_display()


class BatterySerializer(PartBaseSerializer):
    class Meta:
        model = Battery
        fields = common_fields + ['id']


class BatteryHolderSerializer(PartBaseSerializer):
    class Meta:
        model = BatteryHolder
        fields = common_fields + ['id']


class BridgeRectifierSerializer(PartBaseSerializer):
    class Meta:
        model = BridgeRectifier
        fields = common_fields + ['id']


class CapacitorSerializer(PartBaseSerializer):
    capacitor_type = serializers.SerializerMethodField()
    capacitance = serializers.SerializerMethodField()
    voltage = serializers.SerializerMethodField()
    tolerance = serializers.SerializerMethodField()

    class Meta:
        model = Capacitor
        fields = common_fields + ['id', 'capacitor_type', 'capacitance', 'tolerance', 'voltage', 'dielectric_type']

    def get_capacitor_type(self, obj):
        return obj.get_capacitor_type_display()

    def get_capacitance(self, obj):
        return obj.get_capacitance_display()

    def get_voltage(self, obj):
        return obj.get_voltage_display()

    def get_tolerance(self, obj):
        return obj.get_tolerance_display()


class CommonModeChokeSerializer(PartBaseSerializer):
    class Meta:
        model = CommonModeChoke
        fields = common_fields + ['id']


class ConnectorSerializer(PartBaseSerializer):
    class Meta:
        model = Connector
        fields = common_fields + ['id']


class CrystalSerializer(PartBaseSerializer):
    class Meta:
        model = Crystal
        fields = common_fields + ['id']


class DiodeSerializer(PartBaseSerializer):
    class Meta:
        model = Diode
        fields = common_fields + ['id']


class TVSSerializer(PartBaseSerializer):
    class Meta:
        model = TVS
        fields = common_fields + ['id']


class EnclosureSerializer(PartBaseSerializer):
    class Meta:
        model = Enclosure
        fields = common_fields + ['id']


class FerriteBeadSerializer(PartBaseSerializer):
    class Meta:
        model = FerriteBead
        fields = common_fields + ['id']


class InductorSerializer(PartBaseSerializer):
    class Meta:
        model = Inductor
        fields = common_fields + ['id']


class IntegratedCircuitSerializer(PartBaseSerializer):
    supply_voltage = serializers.SerializerMethodField()

    class Meta:
        model = IntegratedCircuit
        fields = common_fields + ['id', 'supply_voltage']

    def get_supply_voltage(self, obj):
        return obj.supply_voltage.get_supply_voltage_display()


class LEDSerializer(PartBaseSerializer):
    class Meta:
        model = LED
        fields = common_fields + ['id']


class ModuleSerializer(PartBaseSerializer):
    class Meta:
        model = Module
        fields = common_fields + ['id']


class ResistorSerializer(PartBaseSerializer):
    resistance = serializers.SerializerMethodField()
    tolerance = serializers.SerializerMethodField()
    power = serializers.SerializerMethodField()

    class Meta:
        model = Resistor
        fields = common_fields + ['id', 'resistance', 'tolerance', 'power']

    def get_resistance(self, obj):
        return obj.resistance.get_resistance_display()

    def get_tolerance(self, obj):
        return obj.resistance.get_tolerance_display()

    def get_power(self, obj):
        return obj.get_power_display()


class SwitchSerializer(PartBaseSerializer):
    class Meta:
        model = Switch
        fields = common_fields + ['id']


class TransistorBipolarSerializer(PartBaseSerializer):
    class Meta:
        model = TransistorBipolar
        fields = common_fields + ['id']


class TransistorMosfetSerializer(PartBaseSerializer):
    class Meta:
        model = TransistorMosfet
        fields = common_fields + ['id']


class PartPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Part: PartBaseSerializer,
        Balun: BalunSerializer,
        Capacitor: CapacitorSerializer,
        IntegratedCircuit: IntegratedCircuitSerializer,
        Resistor: ResistorSerializer
    }
