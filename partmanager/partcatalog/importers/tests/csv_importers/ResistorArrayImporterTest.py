from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.resistor_array import ResistorArray
from decimal import Decimal


class ResistorArrayCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Bourns", full_name="Bourns")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_resistor_arrays.csv')
        csv_importer.export("/tmp/test_resistor_arrays.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = ResistorArray.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RA')
        self.assertEqual(part.manufacturer_part_number, "CAT16-220J4LF")
        self.assertEqual(part.manufacturer.name, "Bourns")
        self.assertEqual(part.series, 'CAT16')
        self.assertEqual(part.series_description, 'Chip Resistor Arrays')
        self.assertEqual(part.description, 'Resistor Array 4 elements, 22Ω ±5%, max. 250mW, max. 50V')
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
        self.assertEqual(part.elements_count, 4)
        self.assertEqual(part.resistance.min, Decimal('20.9'))
        self.assertEqual(part.resistance.typ, Decimal('22'))
        self.assertEqual(part.resistance.max, Decimal('23.1'))
        self.assertEqual(part.power_rating_per_resistor.max, Decimal('5'))
        self.assertEqual(part.power_rating_per_resistor.at_temp, 70)
        self.assertEqual(part.power_rating_package.max, Decimal('0.25'))
        self.assertEqual(part.power_rating_package.at_temp, None)
        self.assertEqual(part.working_voltage.max, 50)
        self.assertEqual(part.overload_voltage.max, 100)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'CAT16-220J4LF')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Bourns")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
