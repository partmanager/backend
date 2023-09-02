import unittest
from decimal import Decimal
from .time_decoder import time_decoder


class TestTimeDecoder(unittest.TestCase):
    def test_time_decoder(self):
        self.assertEqual(Decimal('0.000000000001'), time_decoder("1ps"))
        self.assertEqual(Decimal('0.000000001'), time_decoder("1ns"))
        self.assertEqual(Decimal('0.000001'), time_decoder("1us"))
        self.assertEqual(Decimal('0.001'), time_decoder("1ms"))
        self.assertEqual(Decimal(1), time_decoder("1s"))
        self.assertEqual(Decimal(1000), time_decoder("1ks"))

