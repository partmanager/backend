import unittest
from .tme import decode_tme_barcode


class TestTMEBarcodeDecoder(unittest.TestCase):
    def test_string_decode(self):
        str1 = 'PDG301-5.0-2P12 1PDG301-5.0-02P-12-00A(H) Q20 K17513107/11'
        decoded = decode_tme_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '17513107')
        self.assertEqual(decoded['order_number']['position'], '11')
        self.assertEqual(decoded['invoice'], None)
        self.assertEqual(decoded['distributor_order_number']['text'], 'DG301-5.0-2P12')
        self.assertEqual(decoded['manufacturer_order_number'], 'DG301-5.0-02P-12-00A(H)')
        self.assertEqual(decoded['quantity'], '20')
        self.assertEqual(decoded['manufacturer'], {})

    def test_string2_decode(self):
        str1 = 'PLP38501TS-ADJ/NOPB 1PLP38501TS-ADJ/NOPB Q4 K16537641/3'
        decoded = decode_tme_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '16537641')
        self.assertEqual(decoded['order_number']['position'], '3')
        self.assertEqual(decoded['invoice'], None)
        self.assertEqual(decoded['distributor_order_number']['text'], 'LP38501TS-ADJ/NOPB')
        self.assertEqual(decoded['manufacturer_order_number'], 'LP38501TS-ADJ/NOPB')
        self.assertEqual(decoded['quantity'], '4')
        self.assertEqual(decoded['manufacturer'], {})

    def test_string3_decode(self):
        str1 = 'PSMAJ15A-13-F 1PSMAJ15A-13-F Q25 4LTW K18098201/1'
        decoded = decode_tme_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '18098201')
        self.assertEqual(decoded['order_number']['position'], '1')
        self.assertEqual(decoded['invoice'], None)
        self.assertEqual(decoded['distributor_order_number']['text'], 'SMAJ15A-13-F')
        self.assertEqual(decoded['manufacturer_order_number'], 'SMAJ15A-13-F')
        self.assertEqual(decoded['quantity'], '25')
        self.assertEqual(decoded['manufacturer'], {})

    def test_string4_decode(self):
        str1 = 'PSMD0402-220K-1% 1P0402WGF2203TCE Q200 K18417297/21'
        decoded = decode_tme_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '18417297')
        self.assertEqual(decoded['order_number']['position'], '21')
        self.assertEqual(decoded['invoice'], None)
        self.assertEqual(decoded['distributor_order_number']['text'], 'SMD0402-220K-1%')
        self.assertEqual(decoded['manufacturer_order_number'], '0402WGF2203TCE')
        self.assertEqual(decoded['quantity'], '200')
        self.assertEqual(decoded['manufacturer'], {})

    def test_string5_decode(self):
        str1 = 'P74HC595PW.118 1P74HC595PW,118 Q25 K18416227/6'
        decoded = decode_tme_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '18416227')
        self.assertEqual(decoded['order_number']['position'], '6')
        self.assertEqual(decoded['invoice'], None)
        self.assertEqual(decoded['distributor_order_number']['text'], '74HC595PW.118')
        self.assertEqual(decoded['manufacturer_order_number'], '74HC595PW,118')
        self.assertEqual(decoded['quantity'], '25')
        self.assertEqual(decoded['manufacturer'], {})


if __name__ == '__main__':
    unittest.main()
