from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.connector import Connector


class ConnectorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TE Connectivity", full_name="TE Connectivity")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_connectors.csv')
        csv_importer.export("/tmp/test_connectors.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Connector.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'COB')
        self.assertEqual(part.manufacturer_part_number, "2199230-3")
        self.assertEqual(part.manufacturer.name, "TE Connectivity")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'M.2, 0.5mm pitch, 4.2mm Height, Key B')
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
        self.assertEqual(part.bus_type, 'M.2_B')
        self.assertEqual(part.pin_count, None)
        self.assertEqual(part.row_count, None)
        self.assertEqual(part.pin_spacing, None)
        self.assertEqual(part.row_spacing, None)
        self.assertEqual(part.pin_height, None)
        self.assertEqual(part.pin_height_form_pcb, None)
        self.assertEqual(part.housing_height, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, '2199230-3')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TE Connectivity")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
