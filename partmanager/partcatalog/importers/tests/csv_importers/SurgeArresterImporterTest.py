from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.surge_arrester import SurgeArrester
from decimal import Decimal


class SurgeArresterCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TDK", full_name="TDK")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_surge_arresters.csv')
        csv_importer.export("/tmp/test_surge_arresters.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = SurgeArrester.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'SAR')
        self.assertEqual(part.manufacturer_part_number, "B88069X1023#")
        self.assertEqual(part.manufacturer.name, "TDK")
        self.assertEqual(part.series, 'S30-A75X')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Surge Arrester 75V ±22.5V, max. 400fF @ 1MHz')
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
        self.assertEqual(part.dc_spark_over_voltage.min, Decimal('52.500'))
        self.assertEqual(part.dc_spark_over_voltage.typ, 75)
        self.assertEqual(part.dc_spark_over_voltage.max, Decimal('97.500'))
        self.assertEqual(part.dc_spark_over_voltage.at_temp, None)
        self.assertEqual(part.arc_voltage.min, None)
        self.assertEqual(part.arc_voltage.typ, 8)
        self.assertEqual(part.arc_voltage.max, None)
        self.assertEqual(part.arc_voltage.at_temp, None)
        self.assertEqual(part.glow_voltage.min, None)
        self.assertEqual(part.glow_voltage.typ, 65)
        self.assertEqual(part.glow_voltage.max, None)
        self.assertEqual(part.glow_voltage.at_temp, None)
        self.assertEqual(part.glow_to_arc_transition_current.min, None)
        self.assertEqual(part.glow_to_arc_transition_current.typ, None)
        self.assertEqual(part.glow_to_arc_transition_current.max, Decimal('0.6'))
        self.assertEqual(part.glow_to_arc_transition_current.at_temp, None)
        self.assertEqual(part.insulation_resistance.min, 1000000000)
        self.assertEqual(part.insulation_resistance.typ, None)
        self.assertEqual(part.insulation_resistance.max, None)
        self.assertEqual(part.insulation_resistance.at_voltage, 50)
        self.assertEqual(part.insulation_resistance.at_temp, None)
        self.assertEqual(part.capacitance.min, None)
        self.assertEqual(part.capacitance.typ, None)
        self.assertEqual(part.capacitance.max, Decimal('0.0000000000004'))
        self.assertEqual(part.capacitance.at_frequency, 1000000)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'B88069X1023T203')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TDK")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
