from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models.common import Package
from .models.SOPackage import SOPackage
from .models.ChipCapacitorPackage import ChipCapacitorPackage
from .models.ChipResistorPackage import ChipResistorPackage


common_fields = ['id', 'name']


class PackageBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = common_fields


class SOPackageSerializer(PackageBaseSerializer):
    class Meta:
        model = SOPackage
        fields = ['name', 'type', 'description', 'dimensions']


class ChipCapacitorPackageSerializer(PackageBaseSerializer):
    class Meta:
        model = ChipCapacitorPackage
        fields = '__all__'


class ChipResistorPackageSerializer(PackageBaseSerializer):
    class Meta:
        model = ChipResistorPackage
        fields = '__all__'


class PackagePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        SOPackage: SOPackageSerializer,
        ChipCapacitorPackage: ChipCapacitorPackageSerializer,
        ChipResistorPackage: ChipResistorPackageSerializer
    }