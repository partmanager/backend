from django.db import models
from .packaging import Packaging


class ManufacturerOrderNumber(models.Model):
    manufacturer_order_number = models.CharField(max_length=200)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    packaging = Packaging()
    part = models.ForeignKey('Part', on_delete=models.CASCADE, related_name="manufacturer_order_number_set")
    note = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    # distributorordernumber_set reverse key from DistributorOrderNumber
    # inventoryposition_set reverse key from InventoryPosition

    class Meta:
        unique_together = ['manufacturer', 'manufacturer_order_number']

    def __str__(self):
        return "{}, {}, {}".format(self.manufacturer, self.manufacturer_order_number, self.get_packaging_type_display())

    @staticmethod
    def quadrant_from_str(quadrant_str):
        quadrant = {'Q1': '1', 'Q2': '2', 'Q3': '3', 'Q4': '4'}
        return quadrant[quadrant_str]

    def to_ajax_response(self):
        id_field = self.pk
        result = [{"id": id_field,
                   'part_type': self.part.get_part_type_display(),
                   "manufacturer": self.manufacturer.name,
                   "manufacturer_order_number": self.manufacturer_order_number,
                   "manufacturer_part_number": self.part.manufacturer_part_number,
                   "part_description": self.part.description,
                   "part_package": self.part.get_package_display(),
                   "packaging_type": self.packaging.type,
                   "packaging_code": self.packaging.code,
                   "packaging_quantity": self.packaging.quantity,
                   "packaging": self.packaging.to_dict()
                   }]
        return result
