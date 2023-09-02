from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.display import Display


class DisplayJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestDisplayManufacturer",
                                    full_name="TestDisplayManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_displays.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Display.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'DIS')
        self.assertEqual(part.manufacturer_part_number, "TESTIDISPLAY#")
        self.assertEqual(part.manufacturer.name, "TestDisplayManufacturer")
        self.assertEqual(part.series, 'TestDisplaySeries')
        self.assertEqual(part.series_description, 'Test Display Series')
        self.assertEqual(part.description, 'Display Description')
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
        self.assertEqual(part.symbol.name, 'display')
        #self.assertEqual(part.files,)
        self.assertEqual(part.color, 'red')
        self.assertEqual(part.resolution.width, 128)
        self.assertEqual(part.resolution.height, 64)
        self.assertEqual(part.controller.manufacturer, 'manufacturer')
        self.assertEqual(part.controller.part_number, 'abcd')
        self.assertEqual(part.controller.interface, 'spi')
        self.assertEqual(part.backlight.source, 'led')
        self.assertEqual(part.backlight.color, 'white')

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTDISPLAYA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestDisplayManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
