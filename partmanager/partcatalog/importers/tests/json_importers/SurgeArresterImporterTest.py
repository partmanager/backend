from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.surge_arrester import SurgeArrester
from decimal import Decimal


class SurgeArresterJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestSurgeArresterManufacturer", full_name="TestSurgeArresterManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_surge_arresters.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = SurgeArrester.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'SAR')
        self.assertEqual(part.manufacturer_part_number, "TESTSURGEARRESTER#")
        self.assertEqual(part.manufacturer.name, "TestSurgeArresterManufacturer")
        self.assertEqual(part.series, 'TestSurgeArrester')
        self.assertEqual(part.series_description, 'Test Surge Arrester')
        self.assertEqual(part.description, 'Surge Arrester , max. 400fF @ 1MHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, 'A')
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, 5)
        self.assertEqual(part.storage_conditions.temperature_max, 35)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, 1)
        self.assertEqual(part.symbol.name, 'surge_arrester_2_pin')
        #self.assertEqual(part.files,)
        self.assertEqual(part.dc_spark_over_voltage.min, None)
        self.assertEqual(part.dc_spark_over_voltage.typ, None)
        self.assertEqual(part.dc_spark_over_voltage.max, None)
        self.assertEqual(part.dc_spark_over_voltage.at_temp, None)
        self.assertEqual(part.arc_voltage.min, None)
        self.assertEqual(part.arc_voltage.typ, None)
        self.assertEqual(part.arc_voltage.max, None)
        self.assertEqual(part.arc_voltage.at_temp, None)
        self.assertEqual(part.glow_voltage.min, None)
        self.assertEqual(part.glow_voltage.typ, None)
        self.assertEqual(part.glow_voltage.max, None)
        self.assertEqual(part.glow_voltage.at_temp, None)
        self.assertEqual(part.glow_to_arc_transition_current.min, None)
        self.assertEqual(part.glow_to_arc_transition_current.typ, None)
        self.assertEqual(part.glow_to_arc_transition_current.max, None)
        self.assertEqual(part.glow_to_arc_transition_current.at_temp, None)
        self.assertEqual(part.insulation_resistance.min, None)
        self.assertEqual(part.insulation_resistance.typ, None)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_voltage, None)
        self.assertEqual(part.insulation_resistance.at_temp, None)
        self.assertEqual(part.capacitance.min, None)
        self.assertEqual(part.capacitance.typ, None)
        self.assertEqual(part.capacitance.max, Decimal('0.0000000000004'))
        self.assertEqual(part.capacitance.at_frequency, 1000000)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTSURGEARRESTERA')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestSurgeArresterManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
