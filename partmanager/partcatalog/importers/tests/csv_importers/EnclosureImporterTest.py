from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.enclosure import Enclosure
from decimal import Decimal


class EnclosureCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Kradex", full_name="Kradex")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_enclosures.csv')
        csv_importer.export("/tmp/test_enclosures.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Enclosure.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'E')
        self.assertEqual(part.manufacturer_part_number, "ZD1009J-ABS-V0")
        self.assertEqual(part.manufacturer.name, "Kradex")
        self.assertEqual(part.series, 'ZD')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Enclosure ABS, For DIN rail, 9 modules')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, None)
        self.assertEqual(part.storage_conditions.temperature_max, None)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol, None)
        #self.assertEqual(part.files,)
        self.assertEqual(part.material, Enclosure.Material.ABS)
        self.assertEqual(part.color, Enclosure.Color.WHITE)
        self.assertEqual(part.flame_rating, Enclosure.FlameRating.UNKNOWN)
        self.assertEqual(part.ip_rating, Enclosure.IPRating.UNKNOWN)
        self.assertEqual(part.length.min, None)
        self.assertEqual(part.length.typ, None)
        self.assertEqual(part.length.max, None)
        self.assertEqual(part.width.min, None)
        self.assertEqual(part.width.typ, None)
        self.assertEqual(part.width.max, None)
        self.assertEqual(part.height.min, None)
        self.assertEqual(part.height.typ, None)
        self.assertEqual(part.height.max, None)
        self.assertEqual(part.pcb_length.min, None)
        self.assertEqual(part.pcb_length.typ, None)
        self.assertEqual(part.pcb_length.max, None)
        self.assertEqual(part.pcb_width.min, None)
        self.assertEqual(part.pcb_width.typ, None)
        self.assertEqual(part.pcb_width.max, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'ZD1009J-ABS-V0')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Kradex")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
