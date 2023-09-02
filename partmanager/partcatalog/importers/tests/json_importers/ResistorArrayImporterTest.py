from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.resistor_array import ResistorArray
from decimal import Decimal


class ResistorArrayJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestResistorArrayManufacturer", full_name="TestResistorArrayManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_resistor_arrays.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = ResistorArray.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RA')
        self.assertEqual(part.manufacturer_part_number, "TESTRESISTORARRAY#")
        self.assertEqual(part.manufacturer.name, "TestResistorArrayManufacturer")
        self.assertEqual(part.series, 'TestResistorArraySeries')
        self.assertEqual(part.series_description, 'Test Resistor Array Series')
        self.assertEqual(part.description, 'Resistor Array 4 elements, 1kΩ ±0.05%, max. 500mW, max. 25V')
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
        self.assertEqual(part.symbol.name, 'resistor_array_4')
        #self.assertEqual(part.files,)
        self.assertEqual(part.elements_count, 4)
        self.assertEqual(part.resistance.min, Decimal('999.5'))
        self.assertEqual(part.resistance.typ, Decimal('1000'))
        self.assertEqual(part.resistance.max, Decimal('1000.5'))
        self.assertEqual(part.power_rating_per_resistor.max, Decimal('0.25'))
        self.assertEqual(part.power_rating_per_resistor.at_temp, None)
        self.assertEqual(part.power_rating_package.max, Decimal('0.5'))
        self.assertEqual(part.power_rating_package.at_temp, None)
        self.assertEqual(part.working_voltage.max, 25)
        self.assertEqual(part.overload_voltage.max, 50)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTRESISTORARRAYA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestResistorArrayManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
