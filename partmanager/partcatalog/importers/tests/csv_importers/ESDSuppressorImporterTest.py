from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.esd_suppressor import ESDSuppressor
from decimal import Decimal


class ESDSuppressorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()
        manufacturer = Manufacturer(name="EATON", full_name="EATON")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_esd_suppressors.csv')
        csv_importer.export("/tmp/test_esd_suppressors.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = ESDSuppressor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'ESD')
        self.assertEqual(part.manufacturer_part_number, "PS04LTVA1")
        self.assertEqual(part.manufacturer.name, "EATON")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'ESD Suppressor, Vr=max. 12V')
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
        self.assertEqual(part.rated_voltage.min, None)
        self.assertEqual(part.rated_voltage.typ, 5)
        self.assertEqual(part.rated_voltage.max, 12)
        self.assertEqual(part.rated_voltage.at_temp, None)
        self.assertEqual(part.clamping_voltage.min, None)
        self.assertEqual(part.clamping_voltage.typ, 25)
        self.assertEqual(part.clamping_voltage.max, None)
        self.assertEqual(part.clamping_voltage.at_temp, None)
        self.assertEqual(part.trigger_voltage.min, None)
        self.assertEqual(part.trigger_voltage.typ, 15)
        self.assertEqual(part.trigger_voltage.max, None)
        self.assertEqual(part.trigger_voltage.at_temp, None)
        self.assertEqual(part.capacitance.min, None)
        self.assertEqual(part.capacitance.typ, Decimal('0.00000000000005'))
        self.assertEqual(part.capacitance.max, Decimal('0.00000000000015'))
        self.assertEqual(part.capacitance.at_frequency, 1000000)
        self.assertEqual(part.attenuation.min, None)
        self.assertEqual(part.attenuation.typ, Decimal('0.2'))
        self.assertEqual(part.attenuation.max, None)
        self.assertEqual(part.leakage_current.min, None)
        self.assertEqual(part.leakage_current.typ, None)
        self.assertEqual(part.leakage_current.max, Decimal('0.000'))
        self.assertEqual(part.leakage_current.at_temp, None)
        self.assertEqual(part.esd_pulse_withstand_count, 1000)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'PS04LTVA1')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "EATON")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
