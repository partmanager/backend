from .models import Distributor, DistributorOrderNumber, DistributorManufacturer
from rest_framework import serializers


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ['id', 'name']


class DistributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ['id', 'name', 'website_url', 'part_count', 'part_without_mon_count']


class DistributorOrderNumberSerializer(serializers.ModelSerializer):
    manufacturer_order_number_mon = serializers.SerializerMethodField()

    class Meta:
        model = DistributorOrderNumber
        fields = ['id', 'distributor_order_number_text', 'manufacturer_order_number_text', 'manufacturer_name_text', 'manufacturer_order_number_mon']

    def get_manufacturer_order_number_mon(self, obj):
        if obj.manufacturer_order_number is not None:
            return obj.manufacturer_order_number.manufacturer_order_number


class DistributorOrderNumberDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorOrderNumber
        fields = '__all__'


class DistributorManufacturerSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name')
    manufacturer_full_name = serializers.CharField(source='manufacturer.full_name')

    class Meta:
        model = DistributorManufacturer
        fields = ['id', 'manufacturer_name_text', 'manufacturer', 'manufacturer_name', 'manufacturer_full_name']


class DistributorManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorManufacturer
        fields = ['manufacturer_name_text', 'manufacturer', 'distributor']


class DistributorManufacturerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorManufacturer
        fields = '__all__'
