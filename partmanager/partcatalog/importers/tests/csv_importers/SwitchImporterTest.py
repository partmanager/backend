from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.switch import Switch
from decimal import Decimal


class SwitchCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Ninigi", full_name="Ninigi")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_switches.csv')
        csv_importer.export("/tmp/test_switches.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Switch.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'S')
        self.assertEqual(part.manufacturer_part_number, "TACTM-69N-F")
        self.assertEqual(part.manufacturer.name, "Ninigi")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Tact Switch, pos=1, 50mA, max. 12V')
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
        self.assertEqual(part.switch_type, Switch.SwitchType.TACT_SWITCH)
        self.assertEqual(part.configuration, Switch.ConfigurationChoices.SPST_NO)
        self.assertEqual(part.position_count, 1)
        self.assertEqual(part.pin_pitch.typ, Decimal('0.0045'))
        self.assertEqual(part.switching_voltage.max, Decimal('12'))
        self.assertEqual(part.switching_current.min, None)
        self.assertEqual(part.switching_current.typ, Decimal('0.05'))
        self.assertEqual(part.switching_current.max, None)
        self.assertEqual(part.switching_current.at_temp, None)
        self.assertEqual(part.contact_resistance.min, None)
        self.assertEqual(part.contact_resistance.typ, None)
        self.assertEqual(part.contact_resistance.max, None)
        self.assertEqual(part.contact_resistance.at_temp, None)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, None)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_temp, None)
        self.assertEqual(part.operating_life, 100000)


        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TACTM-69N-F')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Ninigi")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
