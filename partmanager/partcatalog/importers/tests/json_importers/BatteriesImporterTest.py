from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.battery import Battery, BatteryType, BatteryClassification
from decimal import Decimal


class BatteriesJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestBatteryManufacturer", full_name="TestBatteryManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_batteries.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Battery.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'BAT')
        self.assertEqual(part.manufacturer_part_number, "TESTBATTERY#")
        self.assertEqual(part.manufacturer.name, "TestBatteryManufacturer")
        self.assertEqual(part.series, 'TestBatterySeries')
        self.assertEqual(part.series_description, 'Test Battery Series')
        self.assertEqual(part.description, 'Battery, R6 Alkaline')
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
        self.assertEqual(part.symbol.name, "battery")
        #self.assertEqual(part.files,)
        self.assertEqual(part.battery_type, BatteryType.R6)
        self.assertEqual(part.classification, BatteryClassification.ALKALINE)
        self.assertEqual(part.nominal_voltage.min, None)
        self.assertEqual(part.nominal_voltage.typ, 1.5)
        self.assertEqual(part.nominal_voltage.max, None)
        self.assertEqual(part.nominal_voltage.at_temp, None)
        self.assertEqual(part.internal_resistance.min, Decimal('0.15'))
        self.assertEqual(part.internal_resistance.typ, None)
        self.assertEqual(part.internal_resistance.max, Decimal('0.3'))
        self.assertEqual(part.internal_resistance.at_temp, None)
        self.assertEqual(part.capacity_1.min, None)
        self.assertEqual(part.capacity_1.typ, 3)
        self.assertEqual(part.capacity_1.max, None)
        self.assertEqual(part.capacity_1.at_discharge_current, Decimal('0.025'))
        self.assertEqual(part.capacity_1.at_temp, 21)
        self.assertEqual(part.capacity_2.min, None)
        self.assertEqual(part.capacity_2.typ, 2)
        self.assertEqual(part.capacity_2.max, None)
        self.assertEqual(part.capacity_2.at_discharge_current, Decimal('0.25'))
        self.assertEqual(part.capacity_2.at_temp, 21)
        self.assertEqual(part.capacity_3.typ, None)
        self.assertEqual(part.capacity_3.max, None)
        self.assertEqual(part.capacity_3.at_discharge_current, None)
        self.assertEqual(part.capacity_3.at_temp, None)
        self.assertEqual(part.capacity_4.typ, None)
        self.assertEqual(part.capacity_4.max, None)
        self.assertEqual(part.capacity_4.at_discharge_current, None)
        self.assertEqual(part.capacity_4.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTBATTERYA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestBatteryManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
