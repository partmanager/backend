from django.test import TestCase
from partcatalog.importers.json_importer import json_importer
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.inductor import Inductor
from decimal import Decimal


class InductorJsonImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="TestInductorManufacturer", full_name="TestInductorManufacturer")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        json_importer.parts_import('partcatalog/importers/test_data/json/test_inductors.json')
        json_importer.run(dry=False)

    def test_imported_part(self):
        parts = Inductor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'I')
        self.assertEqual(part.manufacturer_part_number, "TESTIND123#")
        self.assertEqual(part.manufacturer.name, "TestInductorManufacturer")
        self.assertEqual(part.series, 'TestInductorSeries')
        self.assertEqual(part.series_description, 'Test Inductor Series')
        self.assertEqual(part.description, 'Inductor, 10nH ±1nH @ 1MHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 105)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, None)
        self.assertEqual(part.symbol.name, 'inductor')
        #self.assertEqual(part.files,)
        self.assertEqual(part.inductance.min, Decimal('0.000000009'))
        self.assertEqual(part.inductance.typ, Decimal('0.000000010'))
        self.assertEqual(part.inductance.max, Decimal('0.000000011'))
        self.assertEqual(part.inductance.at_frequency, 1000000)
        self.assertEqual(part.inductance.at_temp, None)
        self.assertEqual(part.dc_resistance.min, None)
        self.assertEqual(part.dc_resistance.typ, None)
        self.assertEqual(part.dc_resistance.max, None)
        self.assertEqual(part.dc_resistance.at_temp, None)
        self.assertEqual(part.dc_rated_current.min, None)
        self.assertEqual(part.dc_rated_current.typ, None)
        self.assertEqual(part.dc_rated_current.max, None)
        self.assertEqual(part.dc_rated_current.at_temp, None)
        self.assertEqual(part.q_factor.min, None)
        self.assertEqual(part.q_factor.typ, None)
        self.assertEqual(part.q_factor.max, None)
        self.assertEqual(part.q_factor.at_temp, None)
        self.assertEqual(part.q_factor.at_frequency, None)
        self.assertEqual(part.dc_saturation_current_1.min, None)
        self.assertEqual(part.dc_saturation_current_1.typ, None)
        self.assertEqual(part.dc_saturation_current_1.max, None)
        self.assertEqual(part.dc_saturation_current_1.at_temp, None)
        self.assertEqual(part.dc_saturation_current_1.at_inductance_drop, None)
        self.assertEqual(part.dc_saturation_current_2.min, None)
        self.assertEqual(part.dc_saturation_current_2.typ, None)
        self.assertEqual(part.dc_saturation_current_2.max, None)
        self.assertEqual(part.dc_saturation_current_2.at_temp, None)
        self.assertEqual(part.dc_saturation_current_2.at_inductance_drop, None)
        self.assertEqual(part.srf.min, None)
        self.assertEqual(part.srf.typ, None)
        self.assertEqual(part.srf.max, None)
        self.assertEqual(part.srf.at_temp, None)
        self.assertEqual(part.rated_operating_voltage, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, 'TESTIND123A')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "TestInductorManufacturer")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
