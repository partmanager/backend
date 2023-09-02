from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.module import Module


class ModuleCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Hope RF", full_name="Hope RF")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_modules.csv')
        csv_importer.export("/tmp/test_modules.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Module.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'M')
        self.assertEqual(part.manufacturer_part_number, "RFM69HCW-868S2")
        self.assertEqual(part.manufacturer.name, "Hope RF")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'ISM Transceiver 868MHz')
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
        self.assertEqual(part.category, Module.ModuleCategory.RFT)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'RFM69HCW-868S2')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Hope RF")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
