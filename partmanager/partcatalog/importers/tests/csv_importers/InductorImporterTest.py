from django.test import TestCase
from partcatalog.importers.csv_to_json import CSVToJson
from manufacturers.models import Manufacturer
from partcatalog.models.part import Part
from partcatalog.models.inductor import Inductor
from decimal import Decimal


class InductorCSVImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Part.objects.all().delete()

        manufacturer = Manufacturer(name="Wurth Elektronik", full_name="Wurth Elektronik")
        manufacturer.save()

        # Set up non-modified objects used by all test methods
        csv_importer = CSVToJson()
        csv_importer.parts_load('partcatalog/importers/test_data/csv/test_inductors.csv')
        csv_importer.export("/tmp/test_inductors.json")
        csv_importer.run(dry=False)

    def test_imported_part(self):
        parts = Inductor.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.part_type, 'I')
        self.assertEqual(part.manufacturer_part_number, "744314110")
        self.assertEqual(part.manufacturer.name, "Wurth Elektronik")
        self.assertEqual(part.series, '')
        self.assertEqual(part.series_description, '')
        self.assertEqual(part.description, 'Inductor, 1.1uH ±220nH @ 1kHz')
        self.assertEqual(part.production_status, 'UNK')
        self.assertEqual(part.device_marking_code, None)
        self.assertEqual(part.notes, None)
        self.assertEqual(part.comment, None)
        self.assertEqual(part.product_url, None)
        self.assertEqual(part.storage_conditions.temperature_min, -40)
        self.assertEqual(part.storage_conditions.temperature_max, 40)
        self.assertEqual(part.storage_conditions.humidity_min, None)
        self.assertEqual(part.storage_conditions.humidity_max, None)
        self.assertEqual(part.storage_conditions.msl_level, 1)
        self.assertEqual(part.symbol.name, 'inductor_with_core')
        #self.assertEqual(part.files,)
        self.assertEqual(part.inductance.min, Decimal('0.00000088'))
        self.assertEqual(part.inductance.typ, Decimal('0.0000011'))
        self.assertEqual(part.inductance.max, Decimal('0.00000132'))
        self.assertEqual(part.inductance.at_frequency, 100000)
        self.assertEqual(part.inductance.at_temp, None)
        self.assertEqual(part.dc_resistance.min, Decimal('0.0028'))
        self.assertEqual(part.dc_resistance.typ, Decimal('0.0032'))
        self.assertEqual(part.dc_resistance.max, Decimal('0.0035'))
        self.assertEqual(part.dc_resistance.at_temp, 20)
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
        self.assertEqual(part.dc_saturation_current_1.typ, Decimal('13.000'))
        self.assertEqual(part.dc_saturation_current_1.max, None)
        self.assertEqual(part.dc_saturation_current_1.at_temp, None)
        self.assertEqual(part.dc_saturation_current_1.at_inductance_drop, None)
        self.assertEqual(part.dc_saturation_current_2.min, None)
        self.assertEqual(part.dc_saturation_current_2.typ, Decimal('6.000'))
        self.assertEqual(part.dc_saturation_current_2.max, None)
        self.assertEqual(part.dc_saturation_current_2.at_temp, None)
        self.assertEqual(part.dc_saturation_current_2.at_inductance_drop, None)
        self.assertEqual(part.srf.min, None)
        self.assertEqual(part.srf.typ, 135000000)
        self.assertEqual(part.srf.max, None)
        self.assertEqual(part.srf.at_temp, None)
        self.assertEqual(part.rated_operating_voltage, None)

        self.assertEqual(len(part.manufacturer_order_number_set.all()), 1)
        manufacturer_order_number = part.manufacturer_order_number_set.all()[0]
        self.assertEqual(manufacturer_order_number.manufacturer_order_number, '744314110')
        self.assertEqual(manufacturer_order_number.manufacturer.name, "Wurth Elektronik")
        #self.assertEqual(manufacturer_order_number.packaging,)
        self.assertEqual(manufacturer_order_number.part, part)
        self.assertEqual(manufacturer_order_number.note, None)
        self.assertEqual(manufacturer_order_number.description, None)
