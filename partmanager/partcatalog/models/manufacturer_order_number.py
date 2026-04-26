from django.db import models
from .packaging import Packaging
from .choices import ProductionStatus


class ManufacturerOrderNumber(models.Model):
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    MON = models.CharField(max_length=200)
    product = models.ForeignKey('partcatalog.Product', on_delete=models.CASCADE, related_name="manufacturer_order_number_set")
    packaging = Packaging()
    note = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    production_status = models.IntegerField(choices=ProductionStatus.choices, default=ProductionStatus.UNKNOWN)
    EAN13 = models.CharField(max_length=13, blank=True, null=True)
    SKU = models.CharField(max_length=30, blank=True, null=True)
    # distributorordernumber_set reverse key from DistributorOrderNumber
    # inventoryposition_set reverse key from InventoryPosition

    class Meta:
        unique_together = ['manufacturer', 'MON']

    def __str__(self):
        return "{}, {}, {}".format(self.manufacturer, self.MON, self.get_packaging_type_display())

    @staticmethod
    def quadrant_from_str(quadrant_str):
        quadrant = {'Q1': '1', 'Q2': '2', 'Q3': '3', 'Q4': '4'}
        return quadrant[quadrant_str]

    def to_ajax_response(self):
        id_field = self.pk
        result = [{"id": id_field,
                   'part_type': self.product.get_part_type_display(),
                   "manufacturer": self.manufacturer.name,
                   "manufacturer_order_number": self.MON,
                   "manufacturer_part_number": self.product.manufacturer_part_number,
                   "part_description": self.product.description,
                   "part_package": self.product.get_package_display(),
                   "packaging_type": self.packaging.type,
                   "packaging_code": self.packaging.code,
                   "packaging_quantity": self.packaging.quantity,
                   "packaging": self.packaging.to_dict()
                   }]
        return result
