from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.resistor import Resistor
from decimal import Decimal


class ResistorJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestResistorManufacturer", full_name="TestResistorManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_resistors.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Resistor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RTN')
        self.assertEqual(part.manufacturer_part_number, "TESTRESISTOR#")
        self.assertEqual(part.manufacturer.name, "TestResistorManufacturer")
        self.assertEqual(part.series, 'TestResistorSeries')
        self.assertEqual(part.series_description, 'Test Resistor Series')
        self.assertEqual(part.description, '1kΩ ±0.05%, max. 50mW, -10 ppm/°C ~ 10 ppm/°C')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, 5)
        self.assertEqual(part.storage_conditions.temperature_max, 35)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'resistor')
        #self.assertEqual(part.files,)
        self.assertEqual(part.resistance.min, Decimal('999.5'))
        self.assertEqual(part.resistance.typ, Decimal('1000'))
        self.assertEqual(part.resistance.max, Decimal('1000.5'))
        self.assertEqual(part.power.max, Decimal('0.05'))
        self.assertEqual(part.power.at_temp, None)
        self.assertEqual(part.power_derating_temp, None)
        self.assertEqual(part.temperature_coefficient.min, -10)
        self.assertEqual(part.temperature_coefficient.typ, None)
        self.assertEqual(part.temperature_coefficient.max, 10)
        self.assertEqual(part.working_voltage.max, 25)
        self.assertEqual(part.overload_voltage.max, 50)
        self.assertEqual(part.dielectric_withstanding_voltage.max, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTRESISTORA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestResistorManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
