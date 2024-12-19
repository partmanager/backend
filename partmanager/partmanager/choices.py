from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.IntegerChoices):
    EUR = 1, _('EUR')
    USD = 2, _('USD')
    PLN = 3, _('PLN')

    __empty__ = _('(Unknown)')


class MerchandiseType(models.IntegerChoices):
    PART = 1, _('Part')
    SERVICE = 2, _('Service')
    SHIPPING = 3, _('Shipping')

    __empty__ = _('(Unknown)')


class QuantityUnit(models.IntegerChoices):
    PCS = 1, _('pcs')
    KG = 2, _('kg')
    M = 3, _('m')

    __empty__ = _('(Unknown)')


class Status(models.IntegerChoices):
    DATA_PREPARATION = 1, _('Data Preparation')
    ORDERED = 2, _('Ordered')
    FINISHED = 3, _('Finished')

    __empty__ = _('(Unknown)')

