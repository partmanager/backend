from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.capacitor import Capacitor
from decimal import Decimal


class CapacitorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="AVX", full_name="AVX")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_capacitors.csv')
        csv_importer.export("/tmp/test_capacitors.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Capacitor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'MCC')
        self.assertEqual(part.manufacturer_part_number, "04023C104KAT#A")
        self.assertEqual(part.manufacturer.name, "AVX")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Capacitor MLCC 100nF ±10%, max. 25V, X7R')
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
        self.assertEqual(part.capacitance.min, Decimal('0.00000009'))
        self.assertEqual(part.capacitance.typ, Decimal('0.0000001'))
        self.assertEqual(part.capacitance.max, Decimal('0.00000011'))
        self.assertEqual(part.voltage.max, 25)
        self.assertEqual(part.voltage.at_temp, None)
        self.assertEqual(part.endurance, None)
        self.assertEqual(part.rated_ripple_current.max, None)
        self.assertEqual(part.rated_ripple_current.at_temp, None)
        self.assertEqual(part.rated_ripple_current.at_freq, None)
        self.assertEqual(part.dissipation_factor, None)
        self.assertEqual(part.dielectric_type, Capacitor.DielectricType.X7R)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, '04023C104KAT2A')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "AVX")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
