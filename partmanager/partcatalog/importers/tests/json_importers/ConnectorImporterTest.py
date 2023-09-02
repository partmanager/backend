from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.connector import Connector


class ConnectorJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestConnectorManufacturer", full_name="TestConnectorManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_connectors.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Connector.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'COB')
        self.assertEqual(part.manufacturer_part_number, "TESTCONNECTOR#")
        self.assertEqual(part.manufacturer.name, "TestConnectorManufacturer")
        self.assertEqual(part.series, 'TestConnectorSeries')
        self.assertEqual(part.series_description, 'Test Connector Series')
        self.assertEqual(part.description, 'Test SIM Card Connector')
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
        self.assertEqual(part.contact_position, None)
        self.assertEqual(part.bus_type, 'SIM')
        self.assertEqual(part.pin_count, None)
        self.assertEqual(part.row_count, None)
        self.assertEqual(part.pin_spacing, None)
        self.assertEqual(part.row_spacing, None)
        self.assertEqual(part.pin_height, None)
        self.assertEqual(part.pin_height_form_pcb, None)
        self.assertEqual(part.housing_height, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTCONNECTORA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestConnectorManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
