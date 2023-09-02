from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.led import LED
from decimal import Decimal


class LEDCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Lucky Light",
                                    full_name="Lucky Light")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_leds.csv')
        csv_importer.export("/tmp/test_leds.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = LED.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'DLE')
        self.assertEqual(part.manufacturer_part_number, "LL-S194PBC-B4-1B")
        self.assertEqual(part.manufacturer.name, "Lucky Light")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'LED Blue')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 85)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol, None)
        #self.assertEqual(part.files,)
        self.assertEqual(part.continuous_forward_current.min, None)
        self.assertEqual(part.continuous_forward_current.typ, Decimal('0.025'))
        self.assertEqual(part.continuous_forward_current.max, None)
        self.assertEqual(part.peak_forward_current.min, None)
        self.assertEqual(part.peak_forward_current.typ, Decimal('0.1'))
        self.assertEqual(part.peak_forward_current.max, None)
        self.assertEqual(part.forward_voltage.min, Decimal('2.8'))
        self.assertEqual(part.forward_voltage.typ, Decimal('3.4'))
        self.assertEqual(part.forward_voltage.max, Decimal('3.8'))
        self.assertEqual(part.luminous_intensity.min, Decimal('0.02'))
        self.assertEqual(part.luminous_intensity.typ, Decimal('0.04'))
        self.assertEqual(part.luminous_intensity.max, None)
        self.assertEqual(part.viewing_angle_in_deg, 130)
        self.assertEqual(part.reverse_voltage.max, 5)
        self.assertEqual(part.color, 'B')

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'LL-S194PBC-B4-1B')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Lucky Light")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
