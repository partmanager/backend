from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.switch import Switch


class SwitchJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestSwitchManufacturer", full_name="TestSwitchManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_switches.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Switch.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'S')
        self.assertEqual(part.manufacturer_part_number, "TESTSWITCH#")
        self.assertEqual(part.manufacturer.name, "TestSwitchManufacturer")
        self.assertEqual(part.series, 'TestSwitchSeries')
        self.assertEqual(part.series_description, 'Test Switch Series')
        self.assertEqual(part.description, 'Tact Switch, pos=1, 1A, max. 500V')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, 'A')
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, 5)
        self.assertEqual(part.storage_conditions.temperature_max, 35)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, 1)
        self.assertEqual(part.symbol.name, 'switch')
        #self.assertEqual(part.files,)
        self.assertEqual(part.switch_type, Switch.SwitchType.TACT_SWITCH)
        self.assertEqual(part.configuration, Switch.ConfigurationChoices.SPST_NO)
        self.assertEqual(part.position_count, 1)
        self.assertEqual(part.pin_pitch.min, None)
        self.assertEqual(part.pin_pitch.typ, None)
        self.assertEqual(part.pin_pitch.max, None)
        self.assertEqual(part.switching_voltage.max, 500)
        self.assertEqual(part.switching_current.min, None)
        self.assertEqual(part.switching_current.typ, 1)
        self.assertEqual(part.switching_current.max, None)
        self.assertEqual(part.switching_current.at_temp, 23)
        self.assertEqual(part.contact_resistance.min, None)
        self.assertEqual(part.contact_resistance.typ, None)
        self.assertEqual(part.contact_resistance.max, 10)
        self.assertEqual(part.contact_resistance.at_temp, 25)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, 1000000)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_temp, 25)
        self.assertEqual(part.operating_life, 100000)


        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTSWITCHA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestSwitchManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
