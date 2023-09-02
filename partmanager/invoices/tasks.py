from celery import shared_task
from .models import InvoiceItem
from distributors.models import Distributor, DistributorOrderNumber


@shared_task
def update_invoice_item_don_assignments():
    print('updating invoice item DON')

    invoice_items_to_update = InvoiceItem.objects.filter(distributor_order_number__isnull=True,
                                                         distributor_number__isnull=False)
    skip = ['DELIVERY_AUTO']
    request_don = {}
    for ii in invoice_items_to_update:
        try:
            if ii.distributor_number not in skip:
                print(f"Updating {ii}, {ii.distributor_number}")
                don = DistributorOrderNumber.objects.get(distributor=ii.invoice.distributor,
                                                         distributor_order_number_text=ii.distributor_number)
                ii.distributor_order_number = don
                ii.save()
        except DistributorOrderNumber.DoesNotExist as e:
            if ii.invoice.distributor.pk not in request_don:
                request_don[ii.invoice.distributor.pk] = set()
            request_don[ii.invoice.distributor.pk].add(ii.distributor_number)
            print(f"\tDON Missing. {e}")
    print(request_don)
    for key in request_don:
        distributor = Distributor.objects.get(pk=key)
        print(distributor)
#        distributor.request_order_numbers(request_don[key])

