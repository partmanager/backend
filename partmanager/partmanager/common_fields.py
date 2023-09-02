from django.db import models
from composite_field import CompositeField
from .choices import Currency


class Price(CompositeField):
    value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.EUR)

    class Proxy(CompositeField.Proxy):
        def to_dict(self):
            dictionary = {'net_value': str(self.value), 'currency': self.currency}
            return dictionary

        def get_display(self):
            return "{:.4f} {}".format(self.value, Currency(self.currency).name)


class PriceWithTax(CompositeField):
    value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    vat_tax = models.IntegerField(null=True, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.EUR)

    class Proxy(CompositeField.Proxy):
        def to_dict(self):
            dictionary = {'net_value': str(self.value), 'currency': self.currency, 'vat_tax': self.vat_tax}
            return dictionary
