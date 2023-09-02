from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.capacitor import Capacitor
from decimal import Decimal


class CapacitorJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestCapacitorManufacturer", full_name="TestCapacitorManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_capacitors.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Capacitor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'MCC')
        self.assertEqual(part.manufacturer_part_number, "TESTCAP123#")
        self.assertEqual(part.manufacturer.name, "TestCapacitorManufacturer")
        self.assertEqual(part.series, 'TestCap')
        self.assertEqual(part.series_description, 'Test Capacitor series')
        self.assertEqual(part.description, 'Capacitor MLCC 10pF ±1pF, max. 25V, C0G')
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
        self.assertEqual(part.symbol.name, 'capacitor_nonpolar')
        #self.assertEqual(part.files,)
        self.assertEqual(part.capacitance.min, Decimal('0.000000000009'))
        self.assertEqual(part.capacitance.typ, Decimal('0.00000000001'))
        self.assertEqual(part.capacitance.max, Decimal('0.000000000011'))
        self.assertEqual(part.voltage.max, 25)
        self.assertEqual(part.voltage.at_temp, None)
        self.assertEqual(part.endurance, None)
        self.assertEqual(part.rated_ripple_current.max, None)
        self.assertEqual(part.rated_ripple_current.at_temp, None)
        self.assertEqual(part.rated_ripple_current.at_freq, None)
        self.assertEqual(part.dissipation_factor, None)
        self.assertEqual(part.dielectric_type, Capacitor.DielectricType.C0G)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 2)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[1]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTCAP123A')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestCapacitorManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)

        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTCAP123B')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestCapacitorManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
