from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.crystal import Crystal
from decimal import Decimal


class CrystalCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="SR Passives", full_name="SR Passives")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_crystals.csv')
        csv_importer.export("/tmp/test_crystals.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Crystal.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'COS')
        self.assertEqual(part.manufacturer_part_number, "14.31818M-49S-SR")
        self.assertEqual(part.manufacturer.name, "SR Passives")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Crystal, 14.31818MHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 85)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'xtal_2p')
        #self.assertEqual(part.files,)
        self.assertEqual(part.frequency.min, 14317750)
        self.assertEqual(part.frequency.typ, 14318180)
        self.assertEqual(part.frequency.max, 14318609)
        self.assertEqual(part.frequency.tolerance_ppm, None)
        self.assertEqual(part.frequency.at_temp, None)
        self.assertEqual(part.frequency.at_temp_tolerance, None)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.min, -30)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.typ, None)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.max, 30)
        self.assertEqual(part.vibration_mode, 'TO')
        self.assertEqual(part.load_capacitance.min, None)
        self.assertEqual(part.load_capacitance.typ, Decimal('0.000000000016'))
        self.assertEqual(part.load_capacitance.max, None)
        self.assertEqual(part.shunt_capacitance.min, None)
        self.assertEqual(part.shunt_capacitance.typ, None)
        self.assertEqual(part.shunt_capacitance.max, Decimal('0.000000000007'))
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