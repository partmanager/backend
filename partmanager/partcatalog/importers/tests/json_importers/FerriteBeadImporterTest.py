from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.ferrite_bead import FerriteBead
from decimal import Decimal


class FerriteBeadJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestFerriteBeadManufacturer", full_name="TestFerriteBeadManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_ferrite_beads.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = FerriteBead.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'FB')
        self.assertEqual(part.manufacturer_part_number, "TESTFERRITEBEAD#")
        self.assertEqual(part.manufacturer.name, "TestFerriteBeadManufacturer")
        self.assertEqual(part.series, 'TestFerriteBeadSeries')
        self.assertEqual(part.series_description, 'Test Ferrite Bead Series')
        self.assertEqual(part.description, 'Ferrite bead, max. 500mA, max. 0.3mΩ')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -55)
        self.assertEqual(part.storage_conditions.temperature_max, 135)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'ferrite_bead')
        #self.assertEqual(part.files,)
        self.assertEqual(part.impedance_1.min, None)
        self.assertEqual(part.impedance_1.typ, None)
        self.assertEqual(part.impedance_1.max, None)
        self.assertEqual(part.impedance_1.tolerance, None)
        self.assertEqual(part.impedance_1.at_frequency, None)
        self.assertEqual(part.impedance_2.min, None)
        self.assertEqual(part.impedance_2.typ, None)
        self.assertEqual(part.impedance_2.max, None)
        self.assertEqual(part.impedance_2.tolerance, None)
        self.assertEqual(part.impedance_2.at_frequency, None)
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
        self.assertEqual(part.dc_rated_current_1.typ, None)
        self.assertEqual(part.dc_rated_current_1.max, Decimal('0.5'))
        self.assertEqual(part.dc_rated_current_1.at_temp, 25)
        self.assertEqual(part.dc_rated_current_2.min, None)
        self.assertEqual(part.dc_rated_current_2.typ, None)
        self.assertEqual(part.dc_rated_current_2.max, None)
        self.assertEqual(part.dc_rated_current_2.at_temp, None)
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
        self.assertEqual(part.dc_resistance.max, Decimal('0.0003'))

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTFERRITEBEADA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestFerriteBeadManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
