from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.ptc_fuse import PTCFuse
from decimal import Decimal


class PTCFuseJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestPTCFuseManufacturer", full_name="TestPTCFuseManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_PTC_fuses.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = PTCFuse.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'PFU')
        self.assertEqual(part.manufacturer_part_number, "TESTPTCFUSE#")
        self.assertEqual(part.manufacturer.name, "TestPTCFuseManufacturer")
        self.assertEqual(part.series, 'TestPTCFuseSeries')
        self.assertEqual(part.series_description, 'Test PTC Fuse Series')
        self.assertEqual(part.description, 'PTC Fuse, max. 60V')
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
        self.assertEqual(part.symbol.name, 'fuse_ptc')
        #self.assertEqual(part.files,)
        self.assertEqual(part.hold_current.max, None)
        self.assertEqual(part.hold_current.at_temp, None)
        self.assertEqual(part.trip_current.max, None)
        self.assertEqual(part.trip_current.at_temp, None)
        self.assertEqual(part.rated_voltage.max, 60)
        self.assertEqual(part.rated_voltage.at_temp, None)
        self.assertEqual(part.fault_current.max, None)
        self.assertEqual(part.fault_current.at_temp, None)
        self.assertEqual(part.tripped_power_dissipation.min, None)
        self.assertEqual(part.tripped_power_dissipation.typ, None)
        self.assertEqual(part.tripped_power_dissipation.max, None)
        self.assertEqual(part.time_to_trip.max, None)
        self.assertEqual(part.time_to_trip.at_current, None)
        self.assertEqual(part.time_to_trip.at_temp, None)
        self.assertEqual(part.resistance.min, Decimal('3.6'))
        self.assertEqual(part.resistance.typ, None)
        self.assertEqual(part.resistance.max, None)
        self.assertEqual(part.resistance.at_temp, 23)
        self.assertEqual(part.tripped_resistance.min, None)
        self.assertEqual(part.tripped_resistance.typ, None)
        self.assertEqual(part.tripped_resistance.max, None)
#        self.assertEqual(part.tripped_resistance.at_temp, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'SM005-60')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestPTCFuseManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
