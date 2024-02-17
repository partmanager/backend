import decimal
from pathlib import Path
from django.db import models
from django.db.models import Q
from partmanager.choices import MerchandiseType, QuantityUnit
from partmanager.common_fields import Price, NetGrossPrice, PriceWithTax

BOOKKEEPING_TYPE = (
    ('k', 'Track this invoice in bookkeeping'),
    ('m', 'Track as materials'),
    ('s', 'Track as service'),
    ('e', 'Track as equipment'),
    ('p', 'Private use, skip')
)


class Invoice(models.Model):
    number = models.CharField(max_length=250)
    bookkeeping = models.CharField(max_length=1, choices=BOOKKEEPING_TYPE, default='p')  # calculated field
    invoice_date = models.DateField()
    order_date = models.DateField(null=True, blank=True)  # todo remove
    distributor = models.ForeignKey('distributors.Distributor', on_delete=models.PROTECT)
    invoice_file = models.FileField(upload_to='invoices', null=True, blank=True)
    payment_confirmation_file = models.FileField(upload_to='invoices', null=True, blank=True)
    price = NetGrossPrice()  # calculated field
    local_price = NetGrossPrice()  # # calculated field, Price converted to local currency

    # invoiceitem_set -> reverse key from InvoiceItem class

    class Meta:
        unique_together = ['distributor', 'number']
        ordering = ['-invoice_date', 'distributor', 'number']

    @property
    def item_count(self):
        return len(self.invoiceitem_set.all())

    @property
    def all_items_mapped(self):
        return self.invoiceitem_set.filter(
            Q(distributor_order_number__manufacturer_order_number__isnull=True)).count() == 0

    @staticmethod
    def get_by_invoice_number(invoice_number):
        return Invoice.objects.filter(number=invoice_number)

    # def get_invoice_number_display(self):
    #     return "{}: {}".format(self.distributor.name, self.number)

    def get_item(self, manufacturer_order_number, distributor_order_number_text, position):
        invoice_items = None
        if position is not None:
            invoice_items = self.invoiceitem_set.filter(position_in_invoice=position)
        elif distributor_order_number_text:
            invoice_items = self.invoiceitem_set.filter(
                distributor_order_number__distributor_order_number_text=distributor_order_number_text)
        elif manufacturer_order_number:
            invoice_items = self.invoiceitem_set.filter(
                distributor_order_number__manufacturer_order_number=manufacturer_order_number)
            print("Searching invoice:", self.get_invoice_number_display(), " by MON:", manufacturer_order_number,
                  "Found:", invoice_items)
        if len(invoice_items) == 1:
            invoice_item = invoice_items[0]
            if self.__validate_invoice_item(invoice_item, manufacturer_order_number.manufacturer_order_number,
                                            distributor_order_number_text):
                return invoice_item

    @staticmethod
    def __validate_invoice_item(invoice_item, manufacturer_order_number, distributor_order_number_text):
        if distributor_order_number_text is not None and invoice_item.distributor_number != distributor_order_number_text:
            return False
        if manufacturer_order_number is not None and invoice_item.distributor_order_number:
            if invoice_item.distributor_order_number.manufacturer_order_number_text != manufacturer_order_number:
                return False
        return True

    def __str__(self):
        return "{} --> {} <-- {}, {} positions, ({})".format(self.distributor.name, self.number, self.invoice_date,
                                                             self.item_count, self.pk)

    def to_dict(self):
        dictionary = {'distributor': self.distributor.name,
                      'invoice_number': self.number,
                      'bookkeeping': self.bookkeeping,
                      'invoice_date': self.invoice_date.isoformat(),
                      'order_number': self.order_number,
                      'order_date': self.order_date.isoformat() if self.order_date else None,
                      'file': None,
                      'items': []}
        if self.invoice_file:
            dictionary['file'] = {'filename_org': Path(self.invoice_file.name).name,
                                  'filename': Path(self.invoice_file.path).name}
        for invoice_item in self.invoiceitem_set.all():
            dictionary['items'].append(invoice_item.to_dict())
        return dictionary

    def update_calculated_fields(self):
        if len(self.invoiceitem_set.all()):
            bookkeeping = 'p'
            net_price = decimal.Decimal('0')
            gross_price = decimal.Decimal('0')
            for item in self.invoiceitem_set.all():
                net_price += item.price.value
                gross_price += item.price.value * decimal.Decimal(item.price.tax) / decimal.Decimal(100)
                if item.bookkeeping != 'p':
                    bookkeeping = 'k'

            self.price.net = net_price
            self.price.gross = gross_price
            self.price.currency = self.invoiceitem_set.first().currency
            self.bookkeeping = bookkeeping

    def save(self, *args, **kwargs):
        self.update_calculated_fields()
        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=250, null=True, blank=True)
    type = models.IntegerField(choices=MerchandiseType.choices, default=MerchandiseType.PART)
    position_in_invoice = models.IntegerField()
    distributor_number = models.CharField(max_length=250, null=True, blank=True)
    distributor_order_number = models.ForeignKey('distributors.DistributorOrderNumber', on_delete=models.PROTECT,
                                                 null=True, blank=True)
    ordered_quantity = models.IntegerField(null=True, blank=True)
    shipped_quantity = models.IntegerField(null=True, blank=True)
    delivered_quantity = models.IntegerField(null=True, blank=True)
    quantity_unit = models.IntegerField(choices=QuantityUnit.choices, default=QuantityUnit.PCS)
    price = PriceWithTax()
    unit_price = Price()  # calculated field
    bookkeeping = models.CharField(max_length=1, choices=BOOKKEEPING_TYPE, default='p')
    LOT = models.CharField(max_length=20, null=True, blank=True, verbose_name="Lot number")
    ECCN = models.CharField(max_length=20, null=True, blank=True, verbose_name="Export Control Classification Number")
    COO = models.CharField(max_length=20, null=True, blank=True, verbose_name="Country of origin")
    TARIC = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name="Integrated Tariff of the European Community")

    # inventoryposition_set -> reverse key

    class Meta:
        unique_together = ['invoice', 'position_in_invoice']
        ordering = ['invoice', 'position_in_invoice']

    def save(self, *args, **kwargs):
        self.unit_price.currency = self.price.currency
        if self.delivered_quantity is not None and self.shipped_quantity is not None:
            self.unit_price.net = self.price.net / min(self.delivered_quantity, self.shipped_quantity)
        elif self.shipped_quantity:
            self.unit_price.net = self.price.net / self.shipped_quantity
        elif self.delivered_quantity:
            self.unit_price.net = self.price.net / self.delivered_quantity
        else:
            self.unit_price.net = None

        super(InvoiceItem, self).save(*args, **kwargs)

    def get_price_per_unit_display(self):
        return self.unit_price.get_display()

    def get_distributor_display(self):
        return self.invoice.distributor.name

    def get_invoice_number_display(self):
        return self.invoice.get_invoice_number_display()

    def __str__(self):
        if self.distributor_order_number:
            return "{}, {}, {}".format(self.invoice.distributor.name, self.invoice.number, self.distributor_number)
        else:
            return "{}, {}, {} Missing DON".format(self.invoice.distributor.name, self.invoice.number,
                                                   self.distributor_number)

    def to_dict(self):
        dictionary = {'order_number': self.order_number,
                      'position': self.position_in_invoice,
                      'ordered_quantity': self.ordered_quantity,
                      'shipped_quantity': self.shipped_quantity,
                      'quantity_unit': self.quantity_unit,
                      'distributor_number': self.distributor_number,
                      'price': self.price.to_dict(),
                      'bookkeeping': self.bookkeeping,
                      'LOT': self.LOT,
                      'ECCN': self.ECCN,
                      'COO': self.COO,
                      'TARIC': self.TARIC
                      }
        return dictionary


def get_invoice_item(invoice_number, invoice_position):
    invoice = Invoice.get_by_invoice_number(invoice_number)
    if invoice:
        assert len(invoice) == 1, len(invoice)
        try:
            return invoice[0].invoiceitem_set.get(position_in_invoice=invoice_position)
        except InvoiceItem.DoesNotExist:
            return None
