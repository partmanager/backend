from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.fuse import Fuse
from decimal import Decimal


class FuseJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestFuseManufacturer", full_name="TestFuseManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_fuses.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Fuse.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'FUS')
        self.assertEqual(part.manufacturer_part_number, "TESTFUSE#")
        self.assertEqual(part.manufacturer.name, "TestFuseManufacturer")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Fuse, max. 1A, max. 63V')
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
        self.assertEqual(part.symbol.name, 'fuse')
        #self.assertEqual(part.files,)
        self.assertEqual(part.rated_current.max, 1)
        self.assertEqual(part.rated_current.at_temp, None)
        self.assertEqual(part.rated_voltage.max, 63)
        self.assertEqual(part.rated_voltage.at_temp, None)
        self.assertEqual(part.breaking_capacity.max, None)
        self.assertEqual(part.breaking_capacity.at_temp, None)
        self.assertEqual(part.voltage_drop.max, None)
        self.assertEqual(part.voltage_drop.at_temp, None)
        self.assertEqual(part.melting_integral.min, None)
        self.assertEqual(part.melting_integral.typ, None)
        self.assertEqual(part.melting_integral.max, None)
        self.assertEqual(part.melting_integral.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTFUSEA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestFuseManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
