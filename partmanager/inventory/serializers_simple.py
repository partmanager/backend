from rest_framework import serializers

from .models import StorageLocation, StorageLocationFolder, InventoryPosition


class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ['id', 'location', 'folder']


class StorageLocationFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocationFolder
        fields = '__all__'


class InventoryPositionSerializer(serializers.ModelSerializer):
    storage_location = StorageLocationSerializer(read_only=True)

    class Meta:
        model = InventoryPosition
        fields = '__all__'
