from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.relay import Relay
from decimal import Decimal


class RelayCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Relpol", full_name="Relpol")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_relays.csv')
        csv_importer.export("/tmp/test_relays.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Relay.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'RLY')
        self.assertEqual(part.manufacturer_part_number, "RM85-2011-35-1012")
        self.assertEqual(part.manufacturer.name, "Relpol")
        self.assertEqual(part.series, 'RM85')
        self.assertEqual(part.series_description, 'Miniature relays')
        self.assertEqual(part.description, 'Relay 12V 8.4V/30.6V, Spdt, 250V 5V/440V, max. 3A')
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
        self.assertEqual(part.coil_voltage.min, Decimal('8.400'))
        self.assertEqual(part.coil_voltage.typ, 12)
        self.assertEqual(part.coil_voltage.max, Decimal('30.600'))
        self.assertEqual(part.coil_voltage.at_temp, None)
#        self.assertEqual(part.coil_must_release_voltage.max, Decimal('1.200'))
        self.assertEqual(part.coil_must_release_voltage.at_temp, None)
        self.assertEqual(part.coil_resistance.min, 324)
        self.assertEqual(part.coil_resistance.typ, 360)
        self.assertEqual(part.coil_resistance.max, 396)
        self.assertEqual(part.coil_power.min, None)
        self.assertEqual(part.coil_power.typ, Decimal('0.4'))
        self.assertEqual(part.coil_power.max, Decimal('0.48'))
        self.assertEqual(part.configuration, Relay.ConfigurationChoices.SPDT)
        self.assertEqual(part.switching_voltage.min, 5)
        self.assertEqual(part.switching_voltage.typ, 250)
        self.assertEqual(part.switching_voltage.max, 440)
        self.assertEqual(part.switching_current.min, None)
        self.assertEqual(part.switching_current.typ, 16)
        self.assertEqual(part.switching_current.max, 30)
        self.assertEqual(part.switching_current.at_temp, None)
        self.assertEqual(part.contact_resistance.min, None)
        self.assertEqual(part.contact_resistance.typ, None)
        self.assertEqual(part.contact_resistance.max, Decimal('0.1'))
        self.assertEqual(part.operating_life, 30000000)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, None)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_voltage, None)
        self.assertEqual(part.insulation_resistance.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'RM85-2011-35-1012')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Relpol")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
