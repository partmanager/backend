from .models import Invoice, InvoiceItem
from rest_framework import serializers
from inventory.serializers_simple import InventoryPositionSerializer
from distributors.serializers import DistributorOrderNumberDetailSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'bookkeeping_type',
                  'invoice_date',
                  'distributor',
                  'invoice_file',
                  'item_count',
                  'allitems_mapped',
                  'net_price_value']


class InvoiceNumberDistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'number', 'distributor']


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'position_in_invoice', 'ordered_quantity', 'price_value', 'price_currency',
                  'unit_price_value']
        extra_kwargs = {
            'id': {'read_only': True},
            'invoice': {'read_only': True}
        }


class InvoiceItemDetailSerializer(serializers.ModelSerializer):
    invoice = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    extended_price = serializers.SerializerMethodField()
    distributor_order_number = serializers.SerializerMethodField()
    inventory_positions = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'invoice': {'read_only': True}
        }

    def get_invoice(self, obj):
        return {'id': obj.invoice.pk,
                'number': f"{obj.invoice.distributor.name}: {obj.invoice.number}"}

    def get_unit_price(self, obj):
        return {'price': obj.unit_price.value,
                'currency': obj.price.currency}

    def get_extended_price(self, obj):
        return {'price': obj.price.value,
                'currency': obj.price.currency}

    def get_distributor_order_number(self, obj):
        if obj.distributor_order_number:
            response = {'don': obj.distributor_order_number.distributor_order_number_text,
                        'manufacturer': obj.distributor_order_number.manufacturer_name_text,
                        'mon': obj.distributor_order_number.manufacturer_order_number_text}
            if obj.distributor_order_number.manufacturer_order_number:
                manufacturer_order_number = obj.distributor_order_number.manufacturer_order_number
                response['mapped_mon'] = {
                    'manufacturer': manufacturer_order_number.manufacturer.name,
                    'mon': manufacturer_order_number.manufacturer_order_number}
            return response

    def get_inventory_positions(self, obj):
        response = []
        for inventory_position in obj.inventoryposition_set.all():
            inventory = {'storage_location': inventory_position.storage_location.location,
                         'stock_quantity': '{} pcs'.format(inventory_position.stock),
                         'stock_value': inventory_position.get_stock_value_display(),
                         'condition': inventory_position.get_condition_display()}
            response.append(inventory)
        return response


class InvoiceItemDetailWithStorageSerializer(serializers.ModelSerializer):
    inventoryposition_set = InventoryPositionSerializer(many=True, read_only=True)
    distributor_order_number = DistributorOrderNumberDetailSerializer(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'invoice': {'read_only': True}
        }


class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }


class InvoiceWithItemsSerializer(serializers.ModelSerializer):
    invoiceitem_set = InvoiceItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'bookkeeping_type',
                  'invoice_date',
                  'distributor',
                  'invoice_file',
                  'item_count',
                  'allitems_mapped',
                  'net_price_value',
                  'invoiceitem_set']
