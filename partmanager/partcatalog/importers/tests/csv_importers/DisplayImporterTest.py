from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.display import Display


class DisplayCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Display Elektronik",
                                    full_name="Display Elektronik")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_displays.csv')
        csv_importer.export("/tmp/test_displays.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Display.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'DIS')
        self.assertEqual(part.manufacturer_part_number, "DEM 128064N SBH-PW-N")
        self.assertEqual(part.manufacturer.name, "Display Elektronik")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'LCD Display, 128x64, ST7565R')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -30)
        self.assertEqual(part.storage_conditions.temperature_max, 80)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol, None)
        #self.assertEqual(part.files,)
        self.assertEqual(part.color, None)
        self.assertEqual(part.resolution.width, 128)
        self.assertEqual(part.resolution.height, 64)
        self.assertEqual(part.controller.manufacturer, 'Sitronix')
        self.assertEqual(part.controller.part_number, 'ST7565R')
        self.assertEqual(part.controller.interface, 'SPI | 8080 | 6800')
        self.assertEqual(part.backlight.source, 'LED')
        self.assertEqual(part.backlight.color, 'White')

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'DEM 128064N SBH-PW-N/V')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Display Elektronik")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
