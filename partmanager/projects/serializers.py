from .models import Assembly, AssemblyItem, AssemblyJob, Project, ProjectVersion, BOM, BOMItem, Rework
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

    class Meta:
        model = AssemblyItem
        fields = '__all__'


class AssemblyItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyItem
        fields = '__all__'


class BOMItemSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)
    manufacturer_order_number = ManufacturerOrderNumberMONAndIDSerializer(read_only=True)
    group = serializers.ChoiceField(choices=BOMItem.GROUP)

    class Meta:
        model = BOMItem
        fields = ['id', 'group', 'get_group_display', 'designators', 'note', 'part',
                  'manufacturer_order_number', 'part_not_found_fallback']


class BOMItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMItem
        fields = ['id', 'group', 'designators', 'note', 'part', 'manufacturer_order_number']


class BOMItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMItem
        fields = ['id', 'bom', 'group', 'designators', 'note', 'part', 'manufacturer_order_number']


class BOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOM
        fields = ['id', 'project', 'name', 'note', 'description']


class BOMUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOM
        fields = ['id', 'name', 'note', 'description']


class BOMDetailSerializer(serializers.ModelSerializer):
    item_set = BOMItemSerializer(many=True, read_only=True)

    class Meta:
        model = BOM
        fields = ['id', 'name', 'note', 'description', 'item_set']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creation_date']


class ProjectVersionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = ProjectVersion
        fields = ['id', 'project', 'name', 'description', 'creation_date']


class ProjectVersionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ['id', 'project', 'name', 'description', 'creation_date']


class AssemblyJobSerializer(serializers.ModelSerializer):
    project_version = ProjectVersionSerializer(read_only=True)
    class Meta:
        model = AssemblyJob
        fields = ['id', 'name', 'description', 'creation_date', 'status', 'quantity', 'project_version', 'rework']


class AssemblyJobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyJob
        fields = ['id', 'name', 'description', 'creation_date', 'status', 'quantity', 'project_version']


class AssemblySerializer(serializers.ModelSerializer):
    assembly_job = AssemblyJobSerializer(read_only=True)
    project_version = ProjectVersionSerializer(read_only=True)
    class Meta:
        model = Assembly
        fields = ['id', 'project_version', 'assembly_job', 'serial_number', 'name', 'description', 'component_cost', 'build_cost', 'rework_set']


class AssemblyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = ['id', 'project_version', 'assembly_job', 'serial_number', 'name', 'description', 'component_cost', 'build_cost']


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
        fields = ['id', 'name', 'description', 'creation_date', 'projectversion_set']

class ReworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rework
        fields = '__all__'



