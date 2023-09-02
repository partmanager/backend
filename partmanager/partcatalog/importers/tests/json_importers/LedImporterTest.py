from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.led import LED
from decimal import Decimal


class LEDJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestLEDManufacturer",
                                    full_name="TestLEDManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_leds.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = LED.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'DLE')
        self.assertEqual(part.manufacturer_part_number, "TESTLED#")
        self.assertEqual(part.manufacturer.name, "TestLEDManufacturer")
        self.assertEqual(part.series, 'TestLEDSeries')
        self.assertEqual(part.series_description, 'Test LED Series')
        self.assertEqual(part.description, 'LED Red')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 105)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'inductor')
        #self.assertEqual(part.files,)
        self.assertEqual(part.continuous_forward_current.min, None)
        self.assertEqual(part.continuous_forward_current.typ, Decimal('0.02'))
        self.assertEqual(part.continuous_forward_current.max, None)
        self.assertEqual(part.peak_forward_current.min, None)
        self.assertEqual(part.peak_forward_current.typ, Decimal('0.1'))
        self.assertEqual(part.peak_forward_current.max, None)
        self.assertEqual(part.forward_voltage.min, None)
        self.assertEqual(part.forward_voltage.typ, Decimal('1.5'))
        self.assertEqual(part.forward_voltage.max, None)
        self.assertEqual(part.luminous_intensity.min, None)
        self.assertEqual(part.luminous_intensity.typ, Decimal('0.2'))
        self.assertEqual(part.luminous_intensity.max, None)
        self.assertEqual(part.viewing_angle_in_deg, 10)
        self.assertEqual(part.reverse_voltage.max, 10)
        self.assertEqual(part.color, 'R')

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTLEDA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestLEDManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
