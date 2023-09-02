from rest_framework import serializers

from .models import StorageLocation, InventoryPosition


class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ['id', 'location', 'folder']


class InventoryPositionSerializer(serializers.ModelSerializer):
    storage_location = StorageLocationSerializer(read_only=True)

    class Meta:
        model = InventoryPosition
        fields = '__all__'
