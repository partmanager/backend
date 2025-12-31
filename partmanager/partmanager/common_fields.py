import decimal

from django.db import models
from composite_field import CompositeField
from .choices import Currency


class Price(CompositeField):
    net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.EUR)

    class Proxy(CompositeField.Proxy):
        def get_currency_display(self):
            return f"{Currency(self.currency).name}"

        def to_dict(self):
            dictionary = {'net': str(self.net) if self.net is not None else None,
                          'currency': self.currency,
                          'currency_display': self.get_currency_display()}
            return dictionary

        def get_display(self):
            return "{:.4f} {}".format(self.net, Currency(self.currency).name)


class PriceWithTax(CompositeField):
    net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    gross = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    vat_tax = models.IntegerField(null=True, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.EUR)

    class Proxy(CompositeField.Proxy):
        def get_currency_display(self):
            return f"{Currency(self.currency).name}"

        def calculate_gross(self):
            if self.net is not None and self.vat_tax is not None:
                self.tax_amount = self.net * (self.vat_tax / decimal.Decimal(100))
                self.gross = self.net + self.tax_amount

        def to_dict(self):
            dictionary = {'net': str(self.net) if self.net is not None else None,
                          'gross': str(self.gross) if self.gross is not None else None,
                          'vat_tax': self.vat_tax,
                          'currency': self.currency,
                          'currency_display': self.get_currency_display()
                          }
            return dictionary


class NetGrossPrice(CompositeField):
    net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    gross = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.EUR)

    class Proxy(CompositeField.Proxy):
        def to_dict(self):
            dictionary = {'net': str(self.net) if self.net is not None else None,
                          'gross': str(self.gross) if self.net is not None else None,
                          'currency': self.currency,
                          'currency_display': self.get_currency_display()}
            return dictionary

        def get_display(self):
            return "{:.4f} ({:.4f}) {}".format(self.net, self.gross, Currency(self.currency).name)

        def get_currency_display(self):
            return f"{Currency(self.currency).name}"
