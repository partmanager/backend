from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.resistor import Resistor
from decimal import Decimal


class ResistorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TE Connectivity", full_name="TE Connectivity")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_resistors.csv')
        csv_importer.export("/tmp/test_resistors.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Resistor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RTK')
        self.assertEqual(part.manufacturer_part_number, "CRGCQ1206F120R")
        self.assertEqual(part.manufacturer.name, "TE Connectivity")
        self.assertEqual(part.series, 'CRGCQ')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, '12Ω ±1%, max. 250mW')
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
        self.assertEqual(part.resistance.min, Decimal('118.8'))
        self.assertEqual(part.resistance.typ, Decimal('120'))
        self.assertEqual(part.resistance.max, Decimal('121.2'))
        self.assertEqual(part.power.max, Decimal('0.25'))
        self.assertEqual(part.power.at_temp, None)
        self.assertEqual(part.power_derating_temp, None)
        self.assertEqual(part.temperature_coefficient.min, None)
        self.assertEqual(part.temperature_coefficient.typ, None)
        self.assertEqual(part.temperature_coefficient.max, None)
        self.assertEqual(part.working_voltage.max, 200)
        self.assertEqual(part.overload_voltage.max, 400)
        self.assertEqual(part.dielectric_withstanding_voltage.max, 500)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'CRGCQ1206F120R')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TE Connectivity")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
