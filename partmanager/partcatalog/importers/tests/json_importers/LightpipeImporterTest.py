from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.lightpipe import Lightpipe
from decimal import Decimal


class LightpipeJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestLightPipeManufacturer", full_name="TestLightPipeManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_light_pipes.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Lightpipe.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'LPI')
        self.assertEqual(part.manufacturer_part_number, "TESTLIGHTPIPE#")
        self.assertEqual(part.manufacturer.name, "TestLightPipeManufacturer")
        self.assertEqual(part.series, 'TestLightPipeSeries')
        self.assertEqual(part.series_description, 'Test Light Pipe Series')
        self.assertEqual(part.description, 'Light pipe test description')
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
        self.assertEqual(part.symbol.name, 'lightpipe_panelmount_1x')
        #self.assertEqual(part.files,)
        self.assertEqual(part.shape, Lightpipe.ShapeType.ROUND)
        self.assertEqual(part.color, Lightpipe.Color.TRANSPARENT)
        self.assertEqual(part.light_count, 1)
        self.assertEqual(part.length.min, None)
        self.assertEqual(part.length.typ, Decimal('0.006'))
        self.assertEqual(part.length.max, None)
        self.assertEqual(part.panel_cutout_diameter.min, None)
        self.assertEqual(part.panel_cutout_diameter.typ, Decimal('0.003'))
        self.assertEqual(part.panel_cutout_diameter.max, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTLIGHTPIPEA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestLightPipeManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
