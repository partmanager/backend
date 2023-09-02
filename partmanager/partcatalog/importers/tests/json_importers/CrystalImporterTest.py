from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.crystal import Crystal
from decimal import Decimal


class CrystalJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestCrystalManufacturer", full_name="TestCrystalManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_crystals.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Crystal.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'COS')
        self.assertEqual(part.manufacturer_part_number, "TESTCRYSTAL#")
        self.assertEqual(part.manufacturer.name, "TestCrystalManufacturer")
        self.assertEqual(part.series, 'TestCrystalSeries')
        self.assertEqual(part.series_description, 'Test Crystal Series')
        self.assertEqual(part.description, 'Crystal, 8MHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -55)
        self.assertEqual(part.storage_conditions.temperature_max, 125)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, 1)
        self.assertEqual(part.symbol.name, 'oscillator_with_enable_4p')
        #self.assertEqual(part.files,)
        self.assertEqual(part.frequency.min, 7999760)
        self.assertEqual(part.frequency.typ, 8000000)
        self.assertEqual(part.frequency.max, 8000240)
        self.assertEqual(part.frequency.tolerance_ppm, None)
        self.assertEqual(part.frequency.at_temp, None)
        self.assertEqual(part.frequency.at_temp_tolerance, None)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.min, -100)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.typ, None)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.max, 100)
        self.assertEqual(part.vibration_mode, 'TO')
        self.assertEqual(part.load_capacitance.min, None)
        self.assertEqual(part.load_capacitance.typ, Decimal('0.000000000015'))
        self.assertEqual(part.load_capacitance.max, None)
        self.assertEqual(part.shunt_capacitance.min, None)
        self.assertEqual(part.shunt_capacitance.typ, Decimal('0.000000000007'))
        self.assertEqual(part.shunt_capacitance.max, None)
        self.assertEqual(part.esr.min, None)
        self.assertEqual(part.esr.typ, None)
        self.assertEqual(part.esr.max, 60)
        self.assertEqual(part.drive_level.min, None)
        self.assertEqual(part.drive_level.typ, Decimal('0.0001'))
        self.assertEqual(part.drive_level.max, None)
        self.assertEqual(part.ageing.min, None)
        self.assertEqual(part.ageing.typ, None)
        self.assertEqual(part.ageing.max, 5)
        self.assertEqual(part.ageing.at_temp, None)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, 500)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_temp, None)