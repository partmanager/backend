import decimal

from .models import Invoice, InvoiceItem
from partmanager.choices import QuantityUnit
from rest_framework import serializers
from distributors.serializers import DistributorOrderNumberDetailSerializer, DistributorSerializer


class InvoiceMinimalSerializer(serializers.ModelSerializer):
    distributor = DistributorSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'invoice_date',
                  'distributor'
                  ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class InvoiceSerializer(serializers.ModelSerializer):
    distributor = DistributorSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    local_price = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'bookkeeping',
                  'invoice_date',
                  'distributor',
                  'invoice_file',
                  'payment_confirmation_file',
                  'item_count',
                  'all_items_mapped',
                  'price',
                  'local_price']
        extra_kwargs = {
            'id': {'read_only': True},
            'bookkeeping': {'read_only': True}
        }

    def get_price(self, obj):
        return obj.price.to_dict()

    def get_local_price(self, obj):
        return obj.local_price.to_dict()


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['number',
                  'invoice_date',
                  'distributor',
                  'invoice_file',
                  'payment_confirmation_file']


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'position_in_invoice', 'ordered_quantity', 'price_net', 'price_currency',
                  'unit_price_net']
        extra_kwargs = {
            'id': {'read_only': True},
            'invoice': {'read_only': True}
        }


class InvoiceItemDetailSerializer(serializers.ModelSerializer):
    invoice = InvoiceMinimalSerializer(read_only=True)
    unit_price = serializers.SerializerMethodField()
    extended_price = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'unit_price', 'extended_price', 'order_number', 'type',
                  'position_in_invoice', 'ordered_quantity', 'shipped_quantity',
                  'delivered_quantity', 'quantity_unit', 'bookkeeping', 'LOT', 'ECCN', 'COO', 'TARIC',
                  'distributor_order_number']
        extra_kwargs = {
            'id': {'read_only': True},
            'invoice': {'read_only': True}
        }

    def get_unit_price(self, obj):
        return obj.unit_price.to_dict()

    def get_extended_price(self, obj):
        return obj.price.to_dict()


class InvoiceItemDetailWithStorageSerializer(serializers.ModelSerializer):
    invoice = InvoiceMinimalSerializer(read_only=True)
    stock_data = serializers.SerializerMethodField()
    distributor_order_number = DistributorOrderNumberDetailSerializer(read_only=True)
    unit_price = serializers.SerializerMethodField()
    extended_price = serializers.SerializerMethodField()
    local_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    bookkeeping_display = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id',
                  'order_number',
                  'type',
                  'type_display',
                  'position_in_invoice',
                  'bookkeeping',
                  'bookkeeping_display',
                  'invoice',
                  'quantity',
                  'unit_price',
                  'extended_price',
                  'local_price',
                  'stock_data',
                  'distributor_order_number',
                  'LOT',
                  'ECCN',
                  'COO',
                  'TARIC']
        # extra_kwargs = {
        #     'id': {'read_only': True},
        #     'invoice': {'read_only': True}
        # }

    def get_unit_price(self, obj):
        return obj.unit_price.to_dict()

    def get_extended_price(self, obj):
        return obj.price.to_dict()

    def get_local_price(self, obj):
        return obj.local_price.to_dict()

    def get_quantity(self, obj):
        return {'ordered': obj.ordered_quantity,
                'shipped': obj.shipped_quantity,
                'delivered': obj.delivered_quantity,
                'unit': obj.quantity_unit,
                'unit_display': QuantityUnit(obj.quantity_unit).name}

    def get_type_display(self, obj):
        return obj.get_type_display()

    def get_bookkeeping_display(self, obj):
        return obj.get_bookkeeping_display()

    def get_stock_data(self, obj):
        response = {'storage_location': [],
                    'quantity': 0,
                    'value': decimal.Decimal(),
                    'value_currency': None
                    }
        for inventory_position in obj.inventoryposition_set.all():
            response['storage_location'].append(inventory_position.storage_location.location)
            response['quantity'] += inventory_position.stock
            if inventory_position.get_stock_value():
                response['value'] += inventory_position.get_stock_value()['net']
                response['value_currency'] = inventory_position.get_stock_value()['currency_display']
        return response


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
                  'bookkeeping',
                  'invoice_date',
                  'distributor',
                  'invoice_file',
                  'item_count',
                  'all_items_mapped',
                  'price_net',
                  'invoiceitem_set']
