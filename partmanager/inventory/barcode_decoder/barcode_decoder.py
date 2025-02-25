from barcode_decoder import barcode_decoder
from distributors.models import DistributorOrderNumber
from invoices.models import InvoiceItem

def decode_barcode(barcode):
    decoded = barcode_decoder.decode(barcode)
    result = []
    for data in decoded:
        if data and data.is_valid():
            result_tmp = {
                'quantity': data.quantity,
                'manufacturer_order_number': data.mon,
                'distributor_order_number': {},
                'manufacturer': {}
            }
            don = find_don(data)
            result_tmp['distributor_order_number']['don'] = don
            if don and don.manufacturer_order_number:
                result_tmp['manufacturer']['id'] = don.manufacturer_order_number.manufacturer.pk
            result_tmp['invoice'] = find_invoice(data, don)
            result.append(result_tmp)
    return result


def find_don(data):
    try:
        if data.don:
            return DistributorOrderNumber.objects.get(
                distributor__name=data.distributor,
                don=data.don)
        elif data.mon:
            return DistributorOrderNumber.objects.get(
                distributor__name=data.distributor,
                don=data.mon)
        else:
            return None
    except DistributorOrderNumber.DoesNotExist:
        return None


def find_invoice(data, don):
    try:
        if data.invoice:
            invoice = InvoiceItem.objects.get(invoice__distributor__name=data.distributor,
                                              invoice__number=data.invoice['number'].lstrip('0'),
                                              position_in_invoice=data.invoice['position'])
        else:
            invoice = InvoiceItem.objects.get(invoice__distributor__name=data.distributor,
                                              order_number=data.order_number['number'],
                                              distributor_order_number=don)
        return invoice
    except InvoiceItem.DoesNotExist:
        print('Unable to find invoice:', data.invoice, data.order_number)

