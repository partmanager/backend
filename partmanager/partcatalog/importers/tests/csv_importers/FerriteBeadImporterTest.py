from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.ferrite_bead import FerriteBead
from decimal import Decimal


class FerriteBeadCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Murata", full_name="Murata")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_ferrite_beads.csv')
        csv_importer.export("/tmp/test_ferrite_beads.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = FerriteBead.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'FB')
        self.assertEqual(part.manufacturer_part_number, "BLM15HD102BH1#")
        self.assertEqual(part.manufacturer.name, "Murata")
        self.assertEqual(part.series, 'BLM')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Ferrite bead, 1kΩ ±250Ω @ 1MHz, 50mA, max. 1.25Ω')
        self.assertEqual(part.production_status, 'ACT')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, 'https://www.murata.com/en-us/products/productdetail?partno=BLM15HD102BH1%23')
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, None)
        self.assertEqual(part.storage_conditions.temperature_max, None)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'ferrite_bead')
        #self.assertEqual(part.files,)
        self.assertEqual(part.impedance_1.min, Decimal('750.00'))
        self.assertEqual(part.impedance_1.typ, Decimal('1000.00'))
        self.assertEqual(part.impedance_1.max, Decimal('1250.00'))
        self.assertEqual(part.impedance_1.tolerance, 0)
        self.assertEqual(part.impedance_1.at_frequency, 100000000)
        self.assertEqual(part.impedance_2.min, Decimal('1200.00'))
        self.assertEqual(part.impedance_2.typ, Decimal('2000.00'))
        self.assertEqual(part.impedance_2.max, Decimal('2800.00'))
        self.assertEqual(part.impedance_2.tolerance, 0)
        self.assertEqual(part.impedance_2.at_frequency, 1000000000)
        self.assertEqual(part.impedance_3.min, None)
        self.assertEqual(part.impedance_3.typ, None)
        self.assertEqual(part.impedance_3.max, None)
        self.assertEqual(part.impedance_3.tolerance, None)
        self.assertEqual(part.impedance_3.at_frequency, None)
        self.assertEqual(part.impedance_4.min, None)
        self.assertEqual(part.impedance_4.typ, None)
        self.assertEqual(part.impedance_4.max, None)
        self.assertEqual(part.impedance_4.tolerance, None)
        self.assertEqual(part.impedance_4.at_frequency, None)
        self.assertEqual(part.dc_rated_current_1.min, None)
        self.assertEqual(part.dc_rated_current_1.typ, Decimal('0.050'))
        self.assertEqual(part.dc_rated_current_1.max, None)
        self.assertEqual(part.dc_rated_current_1.at_temp, 125)
        self.assertEqual(part.dc_rated_current_2.min, None)
        self.assertEqual(part.dc_rated_current_2.typ,  Decimal('0.020'))
        self.assertEqual(part.dc_rated_current_2.max, None)
        self.assertEqual(part.dc_rated_current_2.at_temp, 150)
        self.assertEqual(part.dc_rated_current_3.min, None)
        self.assertEqual(part.dc_rated_current_3.typ, None)
        self.assertEqual(part.dc_rated_current_3.max, None)
        self.assertEqual(part.dc_rated_current_3.at_temp, None)
        self.assertEqual(part.dc_rated_current_4.min, None)
        self.assertEqual(part.dc_rated_current_4.typ, None)
        self.assertEqual(part.dc_rated_current_4.max, None)
        self.assertEqual(part.dc_rated_current_4.at_temp, None)
        self.assertEqual(part.dc_resistance.min, None)
        self.assertEqual(part.dc_resistance.typ, None)
        self.assertEqual(part.dc_resistance.max, Decimal('1.25'))

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'BLM15HD102BH1B')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Murata")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
