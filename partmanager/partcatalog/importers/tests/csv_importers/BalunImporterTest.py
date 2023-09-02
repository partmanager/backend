from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from partcatalog.models.part import Part
from partcatalog.models.balun import Balun
from manufacturers.models import Manufacturer
from math import radians
from decimal import Decimal


class BalunCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TDK", full_name="TDK")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_balun.csv')
        csv_importer.export("/tmp/test_balun.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Balun.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'BAL')
        self.assertEqual(part.manufacturer_part_number, "HHM17147A1")
        self.assertEqual(part.manufacturer.name, "TDK")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Multilayer Balun for 673-2700MHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, 'https://product.tdk.com/en/search/rf/rf/balun/info?part_no=HHM17147A1')
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 85)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'balun')
        #self.assertEqual(part.files,)
        self.assertEqual(part.technology, Balun.Technology.LTCC)
        self.assertEqual(part.operating_frequency_range.min, 673000000)
        self.assertEqual(part.operating_frequency_range.max, 2700000000)
        self.assertEqual(part.unbalanced_port_impedance.min, None)
        self.assertEqual(part.unbalanced_port_impedance.typ, 50)
        self.assertEqual(part.unbalanced_port_impedance.max, None)
        self.assertEqual(part.unbalanced_port_impedance.tolerance, None)
        self.assertEqual(part.unbalanced_port_impedance.at_frequency, None)
        self.assertEqual(part.balanced_port_impedance.min, None)
        self.assertEqual(part.balanced_port_impedance.typ, 100)
        self.assertEqual(part.balanced_port_impedance.max, None)
        self.assertEqual(part.balanced_port_impedance.tolerance, None)
        self.assertEqual(part.balanced_port_impedance.at_frequency, None)
        self.assertEqual(part.unbalanced_port_return_loss.min, 8)
        self.assertEqual(part.unbalanced_port_return_loss.typ, 9)
        self.assertEqual(part.unbalanced_port_return_loss.max, None)
        self.assertAlmostEqual(float(part.phase_balance.min), radians(165), places=3)
        self.assertAlmostEqual(float(part.phase_balance.typ), radians(190), places=3)
        self.assertAlmostEqual(float(part.phase_balance.max), radians(195), places=3)
        self.assertEqual(part.amplitude_balance.min, -1.5)
        self.assertEqual(part.amplitude_balance.typ, Decimal('-0.8'))
        self.assertEqual(part.amplitude_balance.max, Decimal('1.5'))
        self.assertEqual(part.insertion_loss.min, None)
        self.assertEqual(part.insertion_loss.typ, Decimal('1.62'))
        self.assertEqual(part.insertion_loss.max, Decimal('4.12'))
        self.assertEqual(part.power_rating.min, None)
        self.assertEqual(part.power_rating.typ, None)
        self.assertEqual(part.power_rating.max, 1)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'HHM17147A1')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TDK")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
