from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.battery_holder import BatteryHolder, BatteryType


class BatteryHolderJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestBatteryHolderManufacturer", full_name="TestBatteryHolderManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_battery_holders.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = BatteryHolder.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'BH')
        self.assertEqual(part.manufacturer_part_number, "TESTBATTERYHOLDER#")
        self.assertEqual(part.manufacturer.name, "TestBatteryHolderManufacturer")
        self.assertEqual(part.series, 'TestBatteryHolderSeries')
        self.assertEqual(part.series_description, 'Test Battery Holder Series')
        self.assertEqual(part.description, 'Test Battery holder 3x AA, R6, PCB mount')
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
        self.assertEqual(part.symbol.name, 'battery_holder_3xR6')
        #self.assertEqual(part.files,)
        self.assertEqual(part.battery_type, BatteryType.R6)
        self.assertEqual(part.battery_count, 3)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTBATTERYHOLDERA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestBatteryHolderManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
