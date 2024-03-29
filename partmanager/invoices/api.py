from django.http import JsonResponse
from .models import InvoiceItem


def invoice_items_options_list(request):
    # if request.is_ajax():
    object_list = InvoiceItem.objects.all()

    rows = []
    for invoice_item in object_list:
        name = invoice_item.distributor_order_number.don
        rows.append({
            'id': invoice_item.pk,
            'distributor_id': invoice_item.invoice.distributor.pk,
            'mon_id': invoice_item.distributor_order_number.manufacturer_order_number.pk if invoice_item.distributor_order_number and invoice_item.distributor_order_number.manufacturer_order_number else None,
            'name': name,
            'label': '{}: {}({}), {}, position {} -> {}'.format(invoice_item.invoice.distributor.name,
                                                                invoice_item.invoice.number,
                                                                invoice_item.order_number,
                                                                invoice_item.invoice.invoice_date,
                                                                invoice_item.position_in_invoice,
                                                                name)

        })
    response = {"rows": rows}
    return JsonResponse(response, safe=False)
