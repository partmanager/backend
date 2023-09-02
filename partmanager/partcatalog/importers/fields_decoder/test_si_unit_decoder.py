import unittest
from decimal import Decimal
from .si_unit_decoder import time_decode


class TestSiUnitDecoder(unittest.TestCase):
    def test_time_decoder(self):
        self.assertEqual(Decimal('0.000000000001'), time_decode("1ps"))
        self.assertEqual(Decimal('0.000000001'), time_decode("1ns"))
        self.assertEqual(Decimal('0.000001'), time_decode("1us"))
        self.assertEqual(Decimal('0.001'), time_decode("1ms"))
        self.assertEqual(Decimal(1), time_decode("1s"))
        self.assertEqual(Decimal(1000), time_decode("1ks"))
