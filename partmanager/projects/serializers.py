from .models import Assembly, AssemblyItem, Project, ProjectVersion, BOM, BOMItem
from partcatalog.models.part import Part
from partcatalog.serializers import ManufacturerOrderNumberWithLocationsSerializer, ManufacturerOrderNumberMONAndIDSerializer
from inventory.serializers import InventoryReservationSerializer, InventoryPositionSerializer
from rest_framework import serializers


class PartSerializer(serializers.ModelSerializer):
    manufacturer = serializers.ReadOnlyField(source='manufacturer.name')

    class Meta:
        model = Part
        fields = ['id', 'manufacturer_part_number', 'description', 'manufacturer']


class AssemblyItemSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)
    manufacturer_order_number = ManufacturerOrderNumberWithLocationsSerializer(read_only=True)
    inventoryreservation_set = InventoryReservationSerializer(many=True, read_only=True)
    inventory_positions_set = serializers.SerializerMethodField()

    class Meta:
        model = AssemblyItem
        fields = '__all__'

    def get_inventory_positions_set(self, obj):
        inventory = []
        if obj.part is not None:
            for mon in obj.part.manufacturer_order_number_set.all():
                for inventory_position in mon.inventoryposition_set.all():
                    serializer = InventoryPositionSerializer(inventory_position)
                    inventory.append(serializer.data)
        return inventory


class AssemblySerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    project_version = serializers.ReadOnlyField(source='project.version')

    class Meta:
        model = Assembly
        fields = ['id', 'name', 'quantity', 'description', 'project', 'project_name', 'project_version']


class AssemblyDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    project_version = serializers.ReadOnlyField(source='project.version')
    assembly_item_set = AssemblyItemSerializer(many=True, read_only=True)

    class Meta:
        model = Assembly
        fields = ['id', 'name', 'quantity', 'description', 'project', 'project_name', 'project_version', 'assembly_item_set']


class BOMItemSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)
    manufacturer_order_number = ManufacturerOrderNumberMONAndIDSerializer(read_only=True)
    group = serializers.ChoiceField(choices=BOMItem.GROUP)

    class Meta:
        model = BOMItem
        fields = ['id', 'group', 'get_group_display', 'quantity', 'designators', 'note', 'part',
                  'manufacturer_order_number', 'part_not_found_fallback']


class BOMItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMItem
        fields = ['id', 'group', 'quantity', 'designators', 'note', 'part', 'manufacturer_order_number']


class BOMItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMItem
        fields = ['id', 'bom', 'group', 'quantity', 'designators', 'note', 'part', 'manufacturer_order_number']


class BOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOM
        fields = ['id', 'project', 'name', 'note', 'description', 'multiply']


class BOMUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOM
        fields = ['id', 'name', 'note', 'description', 'multiply']


class BOMDetailSerializer(serializers.ModelSerializer):
    item_set = BOMItemSerializer(many=True, read_only=True)

    class Meta:
        model = BOM
        fields = ['id', 'name', 'note', 'description', 'multiply', 'item_set']


class ProjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ['id', 'project', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ProjectVersionDetailSerializer(serializers.ModelSerializer):
    assembly_set = AssemblySerializer(many=True, read_only=True)
    bom_set = BOMSerializer(many=True, read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectVersion
        fields = ['id', 'project', 'name', 'assembly_set', 'bom_set']


class ProjectDetailSerializer(serializers.ModelSerializer):
    projectversion_set = ProjectVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'projectversion_set']



