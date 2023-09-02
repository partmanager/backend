from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.integrated_circuit import IntegratedCircuit
from decimal import Decimal


class IntegratedCircuitCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Analog Devices",
                                    full_name="Analog Devices")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_integrated_circuits.csv')
        csv_importer.export("/tmp/test_integrated_circuits.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = IntegratedCircuit.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'IRS')
        self.assertEqual(part.manufacturer_part_number, "ADF4360-7")
        self.assertEqual(part.manufacturer.name, "Analog Devices")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Integrated Synthesizer and VCO')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, 'https://www.analog.com/en/products/adf4360-7.html')
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 85)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol, None)
        #self.assertEqual(part.files,)
        self.assertEqual(part.supply_voltage.min, Decimal('3.000'))
        self.assertEqual(part.supply_voltage.typ, None)
        self.assertEqual(part.supply_voltage.max, Decimal('3.600'))

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'ADF4360-7BCPZ')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Analog Devices")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
