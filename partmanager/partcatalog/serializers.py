from rest_framework import serializers

from inventory.serializers import InventoryPositionSerializer
from manufacturers.serializers import ManufacturerSerializer

from .models.part import Part
from .models.balun import Balun
from .models.files import File, FileVersion
from .models.manufacturer_order_number import ManufacturerOrderNumber
from .models.resistor import Resistor


class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    fileversion_set = FileVersionSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = ['id', 'name', 'file_type', 'description', 'url', 'fileversion_set']


class PartSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'manufacturer_part_number', 'description', 'manufacturer', 'storage_temperature_range',
                  'package']


class ManufacturerOrderNumberSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)

    class Meta:
        model = ManufacturerOrderNumber
        fields = ['id', 'manufacturer_order_number', 'packaging_type', 'part']


class ManufacturerOrderNumberMONAndIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerOrderNumber
        fields = ['id', 'manufacturer_order_number']


class ManufacturerOrderNumberWithLocationsSerializer(serializers.ModelSerializer):
    inventoryposition_set = InventoryPositionSerializer(many=True, read_only=True)

    class Meta:
        model = ManufacturerOrderNumber
        fields = ['id', 'manufacturer_order_number', 'part', 'manufacturer', 'inventoryposition_set']


class ResistorTableViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resistor
        fields = '__all__'
