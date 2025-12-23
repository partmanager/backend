import decimal
import logging
from pathlib import Path
from django.db import models
from django.db.models import Q
from partmanager.choices import MerchandiseType, QuantityUnit
from partmanager.common_fields import Price, NetGrossPrice, PriceWithTax
from django.conf import settings
from partmanager.choices import Currency, PaymentMethod

BOOKKEEPING_TYPE = (
    ('k', 'Track this invoice in bookkeeping'),
    ('m', 'Track as materials'),
    ('s', 'Track as service'),
    ('e', 'Track as equipment'),
    ('p', 'Private use, skip')
)

logger = logging.getLogger('invoices')


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=250, help_text="Name of the bank")
    holder_name = models.CharField(max_length=250, help_text="Account holder's name")
    number = models.CharField(max_length=20, unique=True)
    currency = models.IntegerField(choices=Currency.choices)
    distributor = models.ForeignKey('distributors.Distributor', on_delete=models.PROTECT)
    # invoice_set -> reverse field from Invoice model

    class Meta:
        ordering = ['distributor', 'currency', 'bank_name', 'number', 'id']


class PaymentConfirmation(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    confirmation_file = models.FileField(upload_to='paymentConfirm', null=True, blank=True)
    payment_date = models.DateField()
    value = Price()
    payment_method = models.IntegerField(choices=PaymentMethod.choices)
    from_bank_account = models.ForeignKey('BankAccount', related_name="paymentconfirmation_from_set", on_delete=models.PROTECT, null=True)
    to_bank_account = models.ForeignKey('BankAccount', related_name="paymentconfirmation_to_set", on_delete=models.PROTECT, null=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['invoice', 'payment_date', 'id']

    def to_dict(self):
        dictionary = {
            'invoice': {
                'number': self.invoice.number,
                'distributor': self.invoice.distributor.name
            },
            'file': None,
            'payment_date': self.payment_date.isoformat(),
            'value': self.value.to_dict(),
            'method': self.get_payment_method_display(),
            'from_bank_account': self.from_bank_account.number if self.from_bank_account else None,
            'to_bank_account': self.to_bank_account.number if self.to_bank_account else None,
            'note': self.note
        }
        if self.confirmation_file:
            dictionary['file'] = {'filename_org': Path(self.confirmation_file.name).name,
                                  'filename': Path(self.confirmation_file.path).name}
        return dictionary


class InvoiceAttachment(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='invoices')
    description = models.CharField(max_length=250)
    note = models.TextField(null=True, blank=True)


class Invoice(models.Model):
    number = models.CharField(max_length=250)
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    price = NetGrossPrice()  # total amount in sellers currency, used to determine invoice currency
    local_price = NetGrossPrice()  # calculated field, Price converted to local currency. Uses price_exchange_rate
    price_exchange_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    is_income = models.BooleanField(default=False)
    distributor = models.ForeignKey('distributors.Distributor', on_delete=models.PROTECT)
    invoice_file = models.FileField(upload_to='invoices', null=True, blank=True)
    payment_expected_title = models.CharField(max_length=250, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    bookkeeping = models.CharField(max_length=1, choices=BOOKKEEPING_TYPE, default='p')  # calculated field
    status = models.CharField(max_length=10, null=True, blank=True) # calculated field, result of automatic audit
    status_message = models.TextField(null=True, blank=True) # calculated field, result of automatic audit
    # paymentconfirmation_set -> reverse key from PaymentConfirmation class
    # invoiceitem_set -> reverse key from InvoiceItem class

    class Meta:
        unique_together = ['distributor', 'number']
        ordering = ['-invoice_date', 'distributor', 'number']

    @property
    def item_count(self):
        return len(self.invoiceitem_set.all())

    @staticmethod
    def get_by_invoice_number(invoice_number):
        return Invoice.objects.filter(number=invoice_number)

    def get_item(self, manufacturer_order_number, distributor_order_number_text, position):
        invoice_items = None
        if position is not None:
            invoice_items = self.invoiceitem_set.filter(position_in_invoice=position)
        elif distributor_order_number_text:
            invoice_items = self.invoiceitem_set.filter(
                distributor_order_number__don=distributor_order_number_text)
        elif manufacturer_order_number:
            invoice_items = self.invoiceitem_set.filter(
                distributor_order_number__mon=manufacturer_order_number)
            logger.info(f"Searching invoice: {self.get_invoice_number_display()} by MON: {manufacturer_order_number}, Found: {invoice_items}")
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
                      'is_income': self.is_income,
                      'bookkeeping': self.bookkeeping,
                      'invoice_date': self.invoice_date.isoformat(),
                      'due_date': self.due_date.isoformat() if self.due_date else None,
                      'price': self.price.to_dict(),
                      'price_exchange_rate': str(self.price_exchange_rate),
                      'paid': self.paid,
                      'paid_date': self.paid_date.isoformat() if self.paid_date else None,
                      'note': self.note,
                      'file': None,
                      'items': [],
                      'payment_confirmations': []}
        if self.invoice_file:
            dictionary['file'] = {'filename_org': Path(self.invoice_file.name).name,
                                  'filename': Path(self.invoice_file.path).name}
        for invoice_item in self.invoiceitem_set.all():
            dictionary['items'].append(invoice_item.to_dict())
        for payment_confirmation in self.paymentconfirmation_set.all():
            dictionary['payment_confirmations'].append(payment_confirmation.to_dict())
        return dictionary

    def update_calculated_fields(self):
        if self.pk is not None and len(self.invoiceitem_set.all()):
            bookkeeping = 'p'
            for item in self.invoiceitem_set.all():
                if item.bookkeeping != 'p':
                    bookkeeping = 'k'
            self.bookkeeping = bookkeeping

            if self.price.currency == settings.LOCAL_CURRENCY:
                self.local_price = self.price
            else:
                self.local_price.net = self.price.net * self.price_exchange_rate
                self.local_price.gross = self.price.net * self.price_exchange_rate
                self.local_price.currency = settings.LOCAL_CURRENCY

    def validate(self):
        if self.pk is not None and len(self.invoiceitem_set.all()):
            # check if sum of item prices is equal to invoice amount
            price_net = decimal.Decimal(0)
            price_gross = decimal.Decimal(0)
            status_message = ""
            for item in self.invoiceitem_set.all():
                if item.price.currency != self.price.currency:
                    status_message += f"ERROR: Incorrect currency on item {item.position_in_invoice}.\n\r"
                if item.price.net is not None:
                    price_net += item.price.net
                if item.price.gross is not None:
                    price_gross += item.price.gross
            price_gross = price_gross.quantize(decimal.Decimal("1.00"))

            if price_net != self.price.net:
                status_message += f"ERROR: Sum of invoice items net prices is not equal to invoice net amount, calculated: {price_net}.\n\r"
            if price_gross != self.price.gross:
                status_message += f"ERROR: Sum of invoice items gross prices is not equal to invoice gross amount, calculated: {price_gross}.\n\r"
            self.status_message = status_message

    def save(self, *args, **kwargs):
        self.update_calculated_fields()
        self.validate()
        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    position_in_invoice = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    order_number = models.CharField(max_length=250, null=True, blank=True)
    distributor_order_number = models.ForeignKey('distributors.DistributorOrderNumber', on_delete=models.PROTECT)
    ordered_quantity = models.IntegerField(null=True, blank=True)
    shipped_quantity = models.IntegerField(null=True, blank=True)
    delivered_quantity = models.IntegerField(null=True, blank=True)
    quantity_unit = models.IntegerField(choices=QuantityUnit.choices, default=QuantityUnit.PCS)
    price = PriceWithTax()  # price in invoice currency
    local_price = PriceWithTax()  # calculated field, price converted to local currency
    unit_price = Price()  # calculated field, price converted to local currency
    type = models.IntegerField(choices=MerchandiseType.choices, default=MerchandiseType.PART)
    bookkeeping = models.CharField(max_length=1, choices=BOOKKEEPING_TYPE, default='p')
    serial_number = models.CharField(max_length=250, null=True, blank=True, verbose_name="Serial number")
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
        self.price.calculate_gross()
        if self.price.currency == settings.LOCAL_CURRENCY:
            self.local_price = self.price
        else:
            convertion_ratio = self.invoice.price_exchange_rate
            self.local_price.net = self.price.net * convertion_ratio
            self.local_price.gross = self.price.gross * convertion_ratio
            self.local_price.currency = settings.LOCAL_CURRENCY

        self.unit_price.currency = self.local_price.currency
        if self.shipped_quantity is not None and self.shipped_quantity > 0:
            if self.local_price.net is not None:
                if self.delivered_quantity is not None and self.shipped_quantity is not None:
                    self.unit_price.net = self.local_price.net / min(self.delivered_quantity, self.shipped_quantity)
                elif self.shipped_quantity:
                    self.unit_price.net = self.local_price.net / self.shipped_quantity
                elif self.delivered_quantity:
                    self.unit_price.net = self.local_price.net / self.delivered_quantity
                else:
                    self.unit_price.net = None
            else:
                logger.error(f"{self.invoice.number}/{self.position_in_invoice} quantity: {self.shipped_quantity}, local price: {self.local_price}")
        else:
            self.unit_price.net = None

        super(InvoiceItem, self).save(*args, **kwargs)
        self.invoice.save()

    def get_price_per_unit_display(self):
        return self.unit_price.get_display()

    def get_distributor_display(self):
        return self.invoice.distributor.name

    def get_invoice_number_display(self):
        return self.invoice.get_invoice_number_display()

    def __str__(self):
        return "{}, {}, {}".format(self.invoice.distributor.name, self.invoice.number, self.distributor_order_number)

    def to_dict(self):
        dictionary = {'order_number': self.order_number,
                      'position': self.position_in_invoice,
                      'description': self.description,
                      'ordered_quantity': self.ordered_quantity,
                      'shipped_quantity': self.shipped_quantity,
                      'quantity_unit': self.quantity_unit,
                      'distributor_number': self.distributor_order_number.don,
                      'price': self.price.to_dict(),
                      'bookkeeping': self.bookkeeping,
                      'serial_number': self.serial_number,
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
