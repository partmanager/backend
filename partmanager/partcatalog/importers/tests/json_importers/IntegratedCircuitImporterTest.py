from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.integrated_circuit import IntegratedCircuit
from decimal import Decimal


class IntegratedCircuitJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestIntegratedCircuitManufacturer",
                                    full_name="TestIntegratedCircuitManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_integrated_circuits.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = IntegratedCircuit.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'IC')
        self.assertEqual(part.manufacturer_part_number, "TESTIC#")
        self.assertEqual(part.manufacturer.name, "TestIntegratedCircuitManufacturer")
        self.assertEqual(part.series, 'TestICSeries')
        self.assertEqual(part.series_description, 'Test IC series')
        self.assertEqual(part.description, 'IC Description')
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
        self.assertEqual(part.supply_voltage.min, 5)
        self.assertEqual(part.supply_voltage.typ, None)
        self.assertEqual(part.supply_voltage.max, 10)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTICA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestIntegratedCircuitManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
