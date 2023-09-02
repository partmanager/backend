from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.battery import Battery, BatteryType, BatteryClassification
from decimal import Decimal


class BatteriesCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Energizer", full_name="Energizer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_battery.csv')
        csv_importer.export("/tmp/test_battery.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Battery.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'BAT')
        self.assertEqual(part.manufacturer_part_number, "E91 MAX")
        self.assertEqual(part.manufacturer.name, "Energizer")
        self.assertEqual(part.series, 'MAX')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Battery, R6 Alkaline')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, 'https://www.energizer.com/batteries/energizer-max-alkaline-batteries')
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
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'E91 MAX')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Energizer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
