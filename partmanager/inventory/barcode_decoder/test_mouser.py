import unittest
from .mouser import decode_mouser_barcode


class TestMouserBarcodeDecoder(unittest.TestCase):
    def test_string_decode(self):
        str1 = '>[)>06]K21105000]14K004]1PDR331-513AE]q4]11K060439500]4LCN]1VBourns'
        decoded = decode_mouser_barcode(str1)
        self.assertEqual(decoded['order_number']['number'], '21105000')
        self.assertEqual(decoded['order_number']['position'], None)
        self.assertEqual(decoded['invoice']['number'], '060439500')
        self.assertEqual(decoded['invoice']['position'], 4)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded['manufacturer_order_number'], 'DR331-513AE')
        self.assertEqual(decoded['quantity'], 4)
        self.assertEqual(decoded['manufacturer']['name'], 'Bourns')

    def test_string2_decode(self):
        barcode_str = '>[)>06]K21105000]14K019]1PB82432C1105J000]q2]11K060439500]4LHU]1VEPCOS / TDK'
        decoded = decode_mouser_barcode(barcode_str)
        self.assertEqual(decoded['order_number']['number'], '21105000')
        self.assertEqual(decoded['order_number']['position'], None)
        self.assertEqual(decoded['invoice']['number'], '060439500')
        self.assertEqual(decoded['invoice']['position'], 19)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded['manufacturer_order_number'], 'B82432C1105J000')
        self.assertEqual(decoded['quantity'], 2)
        self.assertEqual(decoded['manufacturer']['name'], 'EPCOS / TDK')

    def test_string3_decode(self):
        barcode_str = '>[)>06]K21105000]14K016]1PTYA2520123R3M-10]q5]11K060439500]4LCN]1VLaird Performance Materials'
        decoded = decode_mouser_barcode(barcode_str)
        self.assertEqual(decoded['order_number']['number'], '21105000')
        self.assertEqual(decoded['order_number']['position'], None)
        self.assertEqual(decoded['invoice']['number'], '060439500')
        self.assertEqual(decoded['invoice']['position'], 16)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded['manufacturer_order_number'], 'TYA2520123R3M-10')
        self.assertEqual(decoded['quantity'], 5)
        self.assertEqual(decoded['manufacturer']['name'], 'Laird Performance Materials')

    def test_string4_decode(self):
        barcode_str = '[)>^06]K26161557]14K054]1PPESD3V3S2UT,215]q40]11K069009053]4LCN]1VNexperia^d'
        decoded = decode_mouser_barcode(barcode_str)
        self.assertEqual(decoded['order_number']['number'], '26161557')
        self.assertEqual(decoded['order_number']['position'], None)
        self.assertEqual(decoded['invoice']['number'], '069009053')
        self.assertEqual(decoded['invoice']['position'], 54)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded['manufacturer_order_number'], 'PESD3V3S2UT,215')
        self.assertEqual(decoded['quantity'], 40)
        self.assertEqual(decoded['manufacturer']['name'], 'Nexperia')

    def test_string5_decode(self):
        barcode_str = '[)>^06]k28614977]14K002]1PEMIF03-SIM02M8]Q15]11K073216369]4LCN]1VSTMicro^d'
        decoded = decode_mouser_barcode(barcode_str)
        self.assertEqual(decoded['order_number']['number'], '28614977')
        self.assertEqual(decoded['order_number']['position'], None)
        self.assertEqual(decoded['invoice']['number'], '073216369')
        self.assertEqual(decoded['invoice']['position'], 2)
    #    self.assertEqual(decoded['distributor_order_number']['don'], None)
        self.assertEqual(decoded['manufacturer_order_number'], 'EMIF03-SIM02M8')
        self.assertEqual(decoded['quantity'], 15)
        self.assertEqual(decoded['manufacturer']['name'], 'STMicro')


if __name__ == '__main__':
    unittest.main()
