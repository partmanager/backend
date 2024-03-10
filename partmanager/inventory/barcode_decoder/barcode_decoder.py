import re
from distributors.models import DistributorOrderNumber
from invoices.models import InvoiceItem
from .mouser import decode_mouser_barcode
from .tme import decode_tme_barcode

decoders = [decode_mouser_barcode, decode_tme_barcode]


def decode_barcode(barcode):
    result = []
    for decoder in decoders:
        decoded = decoder(barcode)
        if decoded:
            don = find_don(decoded)
            decoded['distributor_order_number']['don'] = don
            if don and don.manufacturer_order_number:
                decoded['manufacturer']['id'] = don.manufacturer_order_number.manufacturer.pk
            decoded['invoice'] = find_invoice(decoded, don)
            result.append(decoded)
    return result


def find_don(data):
    try:
        if 'text' in data['distributor_order_number']:
            don = DistributorOrderNumber.objects.get(
                distributor__name=data['distributor']['name'],
                don=data['distributor_order_number']['text'])
        elif data['manufacturer_order_number']:
            don = DistributorOrderNumber.objects.get(
                distributor__name=data['distributor']['name'],
                don=data['manufacturer_order_number'])
        else:
            don = None
        return don
    except DistributorOrderNumber.DoesNotExist:
        return None


def find_invoice(data, don):
    try:
        if data['invoice']:
            invoice = InvoiceItem.objects.get(invoice__distributor__name=data['distributor']['name'],
                                              invoice__number=data['invoice']['number'].lstrip('0'),
                                              position_in_invoice=data['invoice']['position'])
        else:
            invoice = InvoiceItem.objects.get(invoice__distributor__name=data['distributor']['name'],
                                              order_number=data['order_number']['number'],
                                              distributor_order_number=don)
        return invoice
    except InvoiceItem.DoesNotExist:
        print('Unable to find invoice:', data['invoice'])

