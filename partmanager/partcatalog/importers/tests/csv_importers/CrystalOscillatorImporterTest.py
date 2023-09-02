from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.crystal_oscillator import CrystalOscillator
from decimal import Decimal


class CrystalOscillatorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Abracon", full_name="Abracon")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_crystal_oscillators.csv')
        csv_importer.export("/tmp/test_crystal_oscillators.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = CrystalOscillator.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'CRO')
        self.assertEqual(part.manufacturer_part_number, "ASE-8.000MHZ-E-#")
        self.assertEqual(part.manufacturer.name, "Abracon")
        self.assertEqual(part.series, 'ASE')
        self.assertEqual(part.series_description, '3.3V CMOS SMD Crystal Oscillator')
        self.assertEqual(part.description, 'Crystal Oscillator, 8MHz')
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
        self.assertEqual(part.frequency.min, None)
        self.assertEqual(part.frequency.typ, 8000000)
        self.assertEqual(part.frequency.max, None)
        self.assertEqual(part.frequency.tolerance_ppm, None)
        self.assertEqual(part.frequency.at_temp, None)
        self.assertEqual(part.frequency.at_temp_tolerance, None)
        self.assertEqual(part.supply_voltage.min, Decimal('3.135'))
        self.assertEqual(part.supply_voltage.typ, Decimal('3.3'))
        self.assertEqual(part.supply_voltage.max, Decimal('3.465'))
        self.assertEqual(part.supply_current.min, None)
        self.assertEqual(part.supply_current.typ, Decimal('0.0025'))
        self.assertEqual(part.supply_current.max, Decimal('0.007'))
        self.assertEqual(part.standby_current.min, None)
        self.assertEqual(part.standby_current.typ, None)
        self.assertEqual(part.standby_current.max, Decimal('0.00001'))
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.min, -100)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.typ, None)
        self.assertEqual(part.frequency_stability_over_operating_temperature_range.max, 100)
        self.assertEqual(part.rise_time.min, None)
        self.assertEqual(part.rise_time.typ, Decimal('0.0000000025'))
        self.assertEqual(part.rise_time.max, Decimal('0.000000004'))
        self.assertEqual(part.fall_time.min, None)
        self.assertEqual(part.fall_time.typ, Decimal('0.0000000025'))
        self.assertEqual(part.fall_time.max, Decimal('0.000000004'))
        self.assertEqual(part.startup_time.min, None)
        self.assertEqual(part.startup_time.typ, Decimal('0.001'))
        self.assertEqual(part.startup_time.max, Decimal('0.002'))
        #self.assertEqual(part.output_load.min, None)
        #self.assertEqual(part.output_load.typ, )
        #self.assertEqual(part.output_load.max, )
        self.assertEqual(part.peak_to_peak_jitter.min, None)
        self.assertEqual(part.peak_to_peak_jitter.typ, Decimal('0.000000000028'))
        self.assertEqual(part.peak_to_peak_jitter.max, None)
        self.assertEqual(part.rms_jitter.min, None)
        self.assertEqual(part.rms_jitter.typ, Decimal('0.0000000000032'))
        self.assertEqual(part.rms_jitter.max, Decimal('0.000000000005'))
        self.assertEqual(part.ageing.min, -3)
        self.assertEqual(part.ageing.typ, None)
        self.assertEqual(part.ageing.max, 3)
        self.assertEqual(part.ageing.at_temp, 25)
        self.assertEqual(part.enable_pin, True)
        self.assertEqual(part.tri_state_output, True)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'ASE-8.000MHZ-E-T')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Abracon")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
