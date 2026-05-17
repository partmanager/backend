from django.db import models
from django.core.exceptions import FieldDoesNotExist  # NOQA
from .choices import ProductionStatus, PART_TYPE
from .files import File
from .fields.operating_conditions import OperatingConditions
from .fields.storage_conditions import StorageConditions
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import ArrayField


class ProductSeries(models.Model):
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


class Product(PolymorphicModel):
    part_type = models.CharField(max_length=3, choices=PART_TYPE, default='UNK')
    generated = models.BooleanField(default=False)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    MPN = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    series = models.ManyToManyField('ProductSeries', blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    #comment = models.TextField(null=True, blank=True) # TODO remove
    product_url = models.URLField(null=True, blank=True) # in case of generic part calculated field pointing to part specs in frontend
    operating_conditions = OperatingConditions()
    storage_conditions = StorageConditions()
    files = models.ManyToManyField(File, blank=True)
    thumbnail = models.ImageField(max_length=250, upload_to='part_catalog/images/', blank=True, null=True)
    images = ArrayField(models.ImageField(max_length=250, upload_to='part_catalog/images/'), blank=True, null=True)

    # generic part fields
    generic = models.BooleanField(default=False)
    filters = models.JSONField(null=True, blank=True)
    MONs = models.ManyToManyField('partcatalog.ManufacturerOrderNumber', related_name="generics", blank=True) # when
    # generic is False this field is calculated. It contains references to ManufacturerOrderNumber model

    # calculated fields
    production_status = models.IntegerField(choices=ProductionStatus.choices, default=ProductionStatus.UNKNOWN) # calculated field

    class Meta:
        unique_together = ['manufacturer', 'MPN']
        ordering = ['manufacturer', 'MPN']
        index_together = [
            ["manufacturer", "MPN"],
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        self.update_calculated_fields()
        super().save(*args, **kwargs)

    def update_calculated_fields(self):
        self._update_production_status_field()
        self._update_MONs_field()

    def _update_production_status_field(self):
        self.production_status = ProductionStatus.OBSOLETE
        for mon in self.MONs.all():
            if mon.production_status != ProductionStatus.OBSOLETE:
                self.production_status = ProductionStatus.IN_PRODUCTION
                break

    def _update_MONs_field(self):
        if not self.generic:
            self.MONs.set(self.manufacturer_order_number_set.all())

    @staticmethod
    def product_type_from_str(connector_str):
        values = {'3DFilament': 'ABS'}
        return values[connector_str]
