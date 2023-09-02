from django.test import TestCase
from decimal import Decimal
import math
from .units_decoder import decode_battery_capacity, decode_capacitance_cond_freq, decode_decibel, decode_dimension,\
    decode_frequency_range, decode_impedance, decode_phase, decode_power, decode_resistance


class ImportersCSVFieldDecoderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_decode_battery_capacity(self):
        csv_field_content = "3000mAh @ Id=25mA, TA=21°C | 2000mAh @ Id=250mA, TA=21°C"
        decoded = decode_battery_capacity(csv_field_content, 'field', 2)
        self.assertTrue(decoded['field_1_min'] is None)
        self.assertEqual(decoded['field_1_typ'], Decimal('3'))
        self.assertTrue(decoded['field_1_max'] is None)
        self.assertEqual(decoded['field_1_at_discharge_current'], Decimal('0.025'))
        self.assertEqual(decoded['field_1_at_temp'], Decimal('21'))
        self.assertTrue(decoded['field_2_min'] is None)
        self.assertEqual(decoded['field_2_typ'], Decimal('2'))
        self.assertTrue(decoded['field_2_max'] is None)
        self.assertEqual(decoded['field_2_at_discharge_current'], Decimal('0.250'))
        self.assertEqual(decoded['field_2_at_temp'], Decimal('21'))

    def test_decode_capacitance_cond_freq(self):
        csv_field_content = "1.5pF @ 10MHz"
        decoded = decode_capacitance_cond_freq(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('0.0000000000015'))
        self.assertTrue(decoded['field_max'] is None)
        self.assertEqual(decoded['field_at_frequency'], Decimal('10000000'))

        csv_field_content = "max. 1.5pF @ 10MHz"
        decoded = decode_capacitance_cond_freq(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertTrue(decoded['field_typ'] is None)
        self.assertEqual(decoded['field_max'], Decimal('0.0000000000015'))
        self.assertEqual(decoded['field_at_frequency'], Decimal('10000000'))

    def test_decode_decibel(self):
        csv_field_content = "20dB"
        decoded = decode_decibel(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('20'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "20dB ±0.1dB"
        decoded = decode_decibel(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('19.9'))
        self.assertEqual(decoded['field_typ'], Decimal('20'))
        self.assertEqual(decoded['field_max'], Decimal('20.1'))

        csv_field_content = "20dB +0.1dB/-1dB"
        decoded = decode_decibel(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('19'))
        self.assertEqual(decoded['field_typ'], Decimal('20'))
        self.assertEqual(decoded['field_max'], Decimal('20.1'))

    def test_decode_dimension(self):
        csv_field_content = "10.5mm"
        decoded = decode_dimension(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('0.0105'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10.5mm ±0.5mm"
        decoded = decode_dimension(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('0.010'))
        self.assertEqual(decoded['field_typ'], Decimal('0.0105'))
        self.assertEqual(decoded['field_max'], Decimal('0.011'))

        csv_field_content = "10.5mm +1mm/-0.5mm"
        decoded = decode_dimension(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('0.010'))
        self.assertEqual(decoded['field_typ'], Decimal('0.0105'))
        self.assertEqual(decoded['field_max'], Decimal('0.0115'))

        # csv_field_content = "10.5mm ±10%"
        # decoded = decode_dimension(csv_field_content, 'field')
        # self.assertEqual(decoded['field_min'], Decimal('0.010'))
        # self.assertEqual(decoded['field_typ'], Decimal('0.0105'))
        # self.assertEqual(decoded['field_max'], Decimal('0.011'))

    def test_decode_frequency_range(self):
        csv_field_content = "10Hz ~ 1GHz"
        decoded = decode_frequency_range(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_max'], Decimal('1000000000'))

    def test_decode_impedance(self):
        csv_field_content = "10.5R"
        decoded = decode_impedance(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10.5R ±0.5R"
        decoded = decode_impedance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11'))

        csv_field_content = "10.5R +1R/-0.5R"
        decoded = decode_impedance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11.5'))

    def test_decode_phase(self):
        csv_field_content = "180°"
        decoded = decode_phase(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertAlmostEqual(decoded['field_typ'], 3.141592653589793, 15)
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10.5° ±0.5°"
        decoded = decode_phase(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], math.radians(Decimal('10')))
        self.assertEqual(decoded['field_typ'], math.radians(Decimal('10.5')))
        self.assertAlmostEqual(decoded['field_max'], math.radians(Decimal('11')), 15)

        csv_field_content = "10.5° +1°/-0.5°"
        decoded = decode_phase(csv_field_content, 'field')
        self.assertAlmostEqual(decoded['field_min'], math.radians(Decimal('10')), 15)
        self.assertAlmostEqual(decoded['field_typ'], math.radians(Decimal('10.5')), 15)
        self.assertAlmostEqual(decoded['field_max'], math.radians(Decimal('11.5')), 15)

    def test_decode_power(self):
        csv_field_content = "18W"
        decoded = decode_power(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('18'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10.5W ±0.5W"
        decoded = decode_power(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11'))

        csv_field_content = "10.5W +1W/-0.5W"
        decoded = decode_power(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11.5'))

    def test_decode_resistance(self):
        csv_field_content = "1R"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('1'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10.5R ±0.5R"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11'))

        csv_field_content = "10.5R +1R/-0.5R"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11.5'))

        csv_field_content = "10.5R +1R"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertTrue(decoded['field_min'] is None)
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertEqual(decoded['field_max'], Decimal('11.5'))

        csv_field_content = "10.5R -0.5R"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('10'))
        self.assertEqual(decoded['field_typ'], Decimal('10.5'))
        self.assertTrue(decoded['field_max'] is None)

        csv_field_content = "10R ±5%"
        decoded = decode_resistance(csv_field_content, 'field')
        self.assertEqual(decoded['field_min'], Decimal('9.5'))
        self.assertEqual(decoded['field_typ'], Decimal('10'))
        self.assertEqual(decoded['field_max'], Decimal('10.5'))

