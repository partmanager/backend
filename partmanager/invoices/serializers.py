import decimal

from .models import BankAccount, Invoice, InvoiceAttachment, InvoiceItem, PaymentConfirmation, INVOICE_STATUS_CHOICES
from partmanager.choices import QuantityUnit
from rest_framework import serializers
from distributors.serializers import DistributorOrderNumberDetailSerializer, DistributorSerializer, DistributorOrderNumberSerializer


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class PaymentConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentConfirmation
        fields = '__all__'


class InvoiceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceAttachment
        fields = '__all__'


class InvoiceMinimalSerializer(serializers.ModelSerializer):
    distributor = DistributorSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'is_income',
                  'invoice_date',
                  'due_date',
                  'paid',
                  'distributor'
                  ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class InvoiceSerializer(serializers.ModelSerializer):
    distributor = DistributorSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    local_price = serializers.SerializerMethodField()
    status = serializers.MultipleChoiceField(choices=INVOICE_STATUS_CHOICES)

    class Meta:
        model = Invoice
        fields = ['id',
                  'number',
                  'is_income',
                  'distributor',
                  'bookkeeping',
                  'invoice_date',
                  'due_date',
                  'distributor',
                  'invoice_file',
                  'price_exchange_rate',
                  'item_count',
                  'price',
                  'local_price',
                  'paid',
                  'paid_date',
                  'note',
                  'status',
                  'status_message',
                  'paymentconfirmation_set']
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
        fields = [
            'number',
            'is_income',
            'invoice_date',
            'due_date',
            'price_net',
            'price_gross',
            'price_currency',
            'paid',
            'note',
            'distributor',
            'invoice_file',
            'price_exchange_rate'
        ]


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
                  'position_in_invoice', 'description', 'ordered_quantity', 'shipped_quantity',
                  'delivered_quantity', 'quantity_unit', 'bookkeeping',
                  'serial_number', 'LOT', 'ECCN', 'COO', 'TARIC',
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
    distributor_order_number = DistributorOrderNumberSerializer(read_only=True)
    unit_price = serializers.SerializerMethodField()
    extended_price = serializers.SerializerMethodField()
    local_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id',
                  'order_number',
                  'type',
                  'type_display',
                  'position_in_invoice',
                  'description',
                  'bookkeeping',
                  'invoice',
                  'quantity',
                  'unit_price',
                  'extended_price',
                  'local_price',
                  'stock_data',
                  'distributor_order_number',
                  'serial_number',
                  'LOT',
                  'ECCN',
                  'COO',
                  'TARIC']

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
