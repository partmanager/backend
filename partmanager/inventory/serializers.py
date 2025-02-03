from rest_framework import serializers

from .models import Category, StorageLocation, InventoryPosition, InventoryReservation, InventoryPositionHistory
from .serializers_simple import StorageLocationSerializer
from invoices.serializers import InvoiceItemSerializer, InvoiceItemDetailSerializer
from manufacturers.serializers import ManufacturerSerializer


class CategorySerializer(serializers.ModelSerializer):
    subcategories_id_set = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories_id_set(self, obj):
        return obj.get_id_set()

class StorageLocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = '__all__'


class InventoryPositionMinimalSerializer(serializers.ModelSerializer):
    storage_location = StorageLocationSerializer(read_only=True)
    invoice = InvoiceItemDetailSerializer(read_only=True)

    class Meta:
        model = InventoryPosition
        fields = ['id', 'stock', 'stock_unit', 'condition', 'status', 'storage_location', 'invoice']


class InventoryPositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryPosition
        fields = '__all__'


class InventoryPositionSerializer(serializers.ModelSerializer):
    storage_location = StorageLocationSerializer(read_only=True)
    invoice = InvoiceItemDetailSerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    reserved_quantity = serializers.SerializerMethodField()
    condition_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    stock_unit_display = serializers.SerializerMethodField()
    alternative_locations = serializers.SerializerMethodField()
    distributors = serializers.SerializerMethodField()
    part = serializers.SerializerMethodField()

    class Meta:
        model = InventoryPosition
        fields = '__all__'

    def get_reserved_quantity(self, obj):
        return obj.get_reserved_quantity()

    def get_condition_display(self, obj):
        return obj.get_condition_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_stock_unit_display(self, obj):
        return obj.get_stock_unit_display()

    def get_distributors(self, obj):
        if obj.mon and obj.mon.distributorordernumber_set:
            return obj.mon.part.distributor_pk_set()

    def get_part(self, obj):
        if obj.mon and obj.mon:
            return obj.mon.part.id

    def get_alternative_locations(self, obj):
        def add_invoice_info(self, dictionary, invoice):
            dictionary['invoice_id'] = invoice.pk
            dictionary['distributor_id'] = invoice.invoice.distributor.pk
            dictionary['distributor'] = invoice.get_distributor_display()  # todo remove
            dictionary['shipped_quantity'] = invoice.shipped_quantity  # todo remove

        if obj.mon:
            other_positions = []
            for position in obj.mon.inventoryposition_set.all():
                if position != obj:
                    position_dict = {'storage_location': position.storage_location.location,
                                     'stock': position.stock,
                                     'condition': position.get_condition_display()}
                    if position.invoice:
                        serializer = InvoiceItemDetailSerializer(position.invoice)
                        position_dict['invoice_item'] = serializer.data

                    other_positions.append(position_dict)
            return other_positions


class StorageLocationWithItemsSerializer(serializers.ModelSerializer):
    inventoryposition_set = InventoryPositionSerializer(many=True, read_only=True)

    class Meta:
        model = StorageLocation
        fields = '__all__'


class InventoryPositionDetailSerializer(serializers.ModelSerializer):
    storage_location = StorageLocationSerializer(read_only=True)
    invoice = InvoiceItemSerializer(read_only=True)
    mon = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    part_pk = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()
    manufacturer_id = serializers.SerializerMethodField()
    available_stock = serializers.SerializerMethodField()
    reserved_quantity = serializers.SerializerMethodField()
    invoice_present = serializers.SerializerMethodField()
    invoice_id = serializers.SerializerMethodField()
    distributor_id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    stock_value = serializers.SerializerMethodField()
    distributor = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    shipped_quantity = serializers.SerializerMethodField()
    distributorordernumber_set = serializers.SerializerMethodField()
    distributors = serializers.SerializerMethodField()
    alternative_locations = serializers.SerializerMethodField()


    class Meta:
        model = InventoryPosition
        fields = '__all__'

    def get_mon(self, obj):
        return {
            'name': obj.mon.manufacturer_order_number if obj.mon else obj.name,
            'description': obj.mon.part.description if obj.mon else obj.description,
            'mon_id': obj.mon.pk if obj.mon else None,
        }

    def get_image(self, obj):
        return str(obj.part.part.icon_image) if obj.part else None

    def get_part_pk(self, obj):
        if obj.part:
            return obj.part.part.pk

    def get_manufacturer(self, obj):
        return obj.get_manufacturer_display()

    def get_manufacturer_id(self, obj):
        return obj.manufacturer.pk if obj.manufacturer else None

    def get_available_stock(self, obj):
        return obj.stock - obj.get_reserved_quantity()

    def get_reserved_quantity(self, obj):
        return obj.get_reserved_quantity()

    def get_invoice_present(self, obj):
        return obj.invoice is not None

    def get_invoice_id(self, obj):
        return obj.invoice.pk if obj.invoice else None

    def get_distributor_id(self, obj):
        return obj.invoice.invoice.distributor.pk if obj.invoice else None

    def get_price(self, obj):
        return obj.invoice.get_price_per_unit_display() if obj.invoice else None  # todo remove

    def get_stock_value(self, obj):
        return obj.get_stock_value_display() if obj.invoice else None  # todo remove

    def get_distributor(self, obj):
        return obj.invoice.get_distributor_display() if obj.invoice else None  # todo remove

    def get_invoice_number(self, obj):
        return obj.invoice.get_invoice_number_display() if obj.invoice else None  # todo remove

    def get_shipped_quantity(self, obj):
        return obj.invoice.shipped_quantity if obj.invoice else None

    def get_distributorordernumber_set(self, obj):
        if obj.part and obj.part.distributorordernumber_set:
            return obj.part.part.distributor_pk_set_urlencoded  # todo delete

    def get_distributors(self, obj):
        if obj.part and obj.part.distributorordernumber_set:
            return obj.part.part.distributor_pk_set()

    def get_alternative_locations(self, obj):
        def add_invoice_info(self, dictionary, invoice):
            dictionary['invoice_id'] = invoice.pk
            dictionary['distributor_id'] = invoice.invoice.distributor.pk
            #dictionary['price'] = invoice.get_price_per_unit_display()  # todo remove
            #dictionary['stock_value'] = self.get_stock_value_display()  # todo remove
            dictionary['distributor'] = invoice.get_distributor_display()  # todo remove
            dictionary['invoice_number'] = invoice.get_invoice_number_display()  # todo remove
            dictionary['shipped_quantity'] = invoice.shipped_quantity  # todo remove

        if obj.part:
            other_positions = []
            for position in obj.part.inventoryposition_set.all():
                if position != obj:
                    position_dict = {'storage_location': position.storage_location.location,
                                     'stock': position.stock,
                                     'condition': position.get_condition_display()}
                    if position.invoice:
                        add_invoice_info(position, position_dict, position.invoice)
                    other_positions.append(position_dict)
            return other_positions


class InventoryReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryReservation
        fields = '__all__'


class InventoryPositionHistorySerializer(serializers.ModelSerializer):
    storage_location = serializers.CharField(source='storage_location.location', read_only=True)

    class Meta:
        model = InventoryPositionHistory
        fields = '__all__'
