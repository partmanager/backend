from django.utils.translation import gettext_lazy as _
from django.db import models
from .part import Part


class Module(Part):
    class ModuleCategory(models.TextChoices):
        RF = 'RF', _('RF Module')
        RFT = 'RFT', _('RF Transceiver')
        SBC = 'SBC', _('Single board computer')
        WIF = 'WIF', _('WI-FI Module')
        LTE = 'LTE', _('LTE Modem')
        OTH = 'OTH', _('Other')

        @staticmethod
        def from_str(tolerance_str):
            values = {'RF Module': 'RF', 'RF Transceiver': 'RFT', 'Single board computer': 'SBC', 'WIFI module': 'WIF',
                      'LTE Modem': 'LTE'}
            return values[tolerance_str]

    part_type_subset = ['M']
    category = models.CharField(max_length=3, choices=ModuleCategory.choices, default=ModuleCategory.OTH)

    custom_fields = {'Category': 'category'}
    fields = {**Part.fields_begin, **custom_fields, **Part.fields_end}

    def to_view_ajax_response(self):
        ajax = Part.to_view_ajax_response(self)
        ajax[0]["category"] = self.get_category_display()
        return ajax
