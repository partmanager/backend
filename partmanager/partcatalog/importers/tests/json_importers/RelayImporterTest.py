from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.relay import Relay
from decimal import Decimal


class RelayJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestRelayManufacturer", full_name="TestRelayManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_relays.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Relay.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RLY')
        self.assertEqual(part.manufacturer_part_number, "TESTRELAY#")
        self.assertEqual(part.manufacturer.name, "TestRelayManufacturer")
        self.assertEqual(part.series, 'TestRelaySeries')
        self.assertEqual(part.series_description, 'TestRelaySeries')
        self.assertEqual(part.description, 'Relay 12V, Spdt')
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
        self.assertEqual(part.symbol.name, 'relay_spst_6p')
        #self.assertEqual(part.files,)
        self.assertEqual(part.coil_voltage.min, None)
        self.assertEqual(part.coil_voltage.typ, 12)
        self.assertEqual(part.coil_voltage.max, None)
        self.assertEqual(part.coil_voltage.at_temp, None)
        self.assertEqual(part.coil_must_release_voltage.max, None)
        self.assertEqual(part.coil_must_release_voltage.at_temp, None)
        self.assertEqual(part.coil_resistance.min, None)
        self.assertEqual(part.coil_resistance.typ, None)
        self.assertEqual(part.coil_resistance.max, None)
        self.assertEqual(part.coil_power.typ, None)
        self.assertEqual(part.coil_power.max, None)
        self.assertEqual(part.coil_power.max, None)
        self.assertEqual(part.configuration, Relay.ConfigurationChoices.SPDT)
        self.assertEqual(part.switching_voltage.min, None)
        self.assertEqual(part.switching_voltage.typ, None)
        self.assertEqual(part.switching_voltage.max, None)
        self.assertEqual(part.switching_current.min, None)
        self.assertEqual(part.switching_current.typ, None)
        self.assertEqual(part.switching_current.max, None)
        self.assertEqual(part.switching_current.at_temp, None)
        self.assertEqual(part.contact_resistance.min, None)
        self.assertEqual(part.contact_resistance.typ, None)
        self.assertEqual(part.contact_resistance.max, None)
        self.assertEqual(part.operating_life, None)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, None)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_voltage, None)
        self.assertEqual(part.insulation_resistance.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTRELAYA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestRelayManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
