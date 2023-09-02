from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.ptc_fuse import PTCFuse
from decimal import Decimal


class PTCFuseCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="ECE", full_name="ECE")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_ptc_fuses.csv')
        csv_importer.export("/tmp/test_ptc_fuses.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = PTCFuse.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'PFU')
        self.assertEqual(part.manufacturer_part_number, "SM005-60")
        self.assertEqual(part.manufacturer.name, "ECE")
        self.assertEqual(part.series, 'SM')
        self.assertEqual(part.series_description, 'Surface mount PTC SM (1210) model')
        self.assertEqual(part.description, 'PTC Fuse, Ih=max. 50mA, max. 60V')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, '5')
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, 'https://www.ece.com.tw/en/resettable-fuse/resettable-fuse/268')
        self.assertEqual(part.storage_conditions.temperature_min, None)
        self.assertEqual(part.storage_conditions.temperature_max, None)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'fuse_ptc')
        #self.assertEqual(part.files,)
        self.assertEqual(part.hold_current.max, Decimal('0.05000'))
        self.assertEqual(part.hold_current.at_temp, None)
        self.assertEqual(part.trip_current.max, Decimal('0.12000'))
        self.assertEqual(part.trip_current.at_temp, None)
        self.assertEqual(part.rated_voltage.max, 60)
        self.assertEqual(part.rated_voltage.at_temp, None)
        self.assertEqual(part.fault_current.max, Decimal('100.00000'))
        self.assertEqual(part.fault_current.at_temp, None)
        self.assertEqual(part.tripped_power_dissipation.min, None)
        self.assertEqual(part.tripped_power_dissipation.typ, Decimal('0.600000'))
        self.assertEqual(part.tripped_power_dissipation.max, None)
        self.assertEqual(part.time_to_trip.max, Decimal('1.500'))
        self.assertEqual(part.time_to_trip.at_current, Decimal('0.250'))
        self.assertEqual(part.time_to_trip.at_temp, None)
        self.assertEqual(part.resistance.min, Decimal('3.6'))
        self.assertEqual(part.resistance.typ, None)
        self.assertEqual(part.resistance.max, None)
        self.assertEqual(part.resistance.at_temp, 23)
        self.assertEqual(part.tripped_resistance.min, None)
        self.assertEqual(part.tripped_resistance.typ, None)
        self.assertEqual(part.tripped_resistance.max, Decimal('50.0000'))
#        self.assertEqual(part.tripped_resistance.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'SM005-60')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "ECE")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
