import decimal
import logging

from invoices.models import Invoice, InvoiceItem
from distributors.models import Distributor, DistributorOrderNumber
from django.db import IntegrityError
from django.core.files import File
from partmanager.choices import Currency

logger = logging.getLogger('invoices')


class InvoiceImporterBase:
    def __init__(self):
        self.dry = False
        self.DON_to_update = []

    def update_or_create_items(self, distributor, invoice_items):
        self.request_missing_distributor_order_numbers(distributor, invoice_items)
        for item in invoice_items:
            self.update_or_create_invoice_item(distributor, item['invoice_model'], item)

    def create_invoice(self, distributor, invoice_dict, files_dir):
        invoice = Invoice(number=invoice_dict['invoice_number'],
                          bookkeeping=invoice_dict['bookkeeping'],
                          distributor=distributor,
                          invoice_date=invoice_dict['invoice_date'])
        if not self.dry:
            invoice.save()
            logger.info('New invoice was created: %s', invoice.number)
            if 'file' in invoice_dict and invoice_dict['file']:
                f = open(files_dir + '/' + invoice_dict['file']['filename'], mode='rb')
                django_file = File(f)
                invoice.invoice_file.save(invoice_dict['file']['filename'], django_file)
        return invoice

    def get_or_create_invoice(self, distributor, invoice_dict, files_dir):
        invoices = Invoice.get_by_invoice_number(invoice_dict['invoice_number'])
        logger.debug(f'{invoices}')
        if invoices:
            for invoice in invoices:
                if invoice.distributor == distributor:
                    logger.info('Invoice already exist')
                    return invoice
        return self.create_invoice(distributor, invoice_dict, files_dir)

    def request_missing_distributor_order_numbers(self, distributor, positions):
        missing_list = []
        for position in positions:
            distributor_order_number = distributor.get_order_number(position['distributor_number'])
            if distributor_order_number is None and position['distributor_number'] not in missing_list:
                missing_list.append(position['distributor_number'])
        if len(missing_list) > 0:
            try:
                distributor.request_order_numbers(missing_list)
            except Exception as e:
                logger.error(f"Unable to request data from distributor, exception: {e}. Affected parts {missing_list}")

    def import_invoice_from_dict(self, invoice_dict, files_dir):
        distributor = Distributor.get_by_name(invoice_dict['distributor'])
        if distributor:
            #self.request_missing_distributor_order_numbers(distributor, invoice_dict['items'])
            db_invoice = self.get_or_create_invoice(distributor, invoice_dict, files_dir)
            for position in invoice_dict['items']:
                invoice_item = self.create_invoice_item(distributor, db_invoice, position)
                # try:
                #     if not self.dry:
                #         invoice_item.save()
                # except IntegrityError as e:
                #     logger.error(e)
            db_invoice.save()
        else:
            logger.error(f"Unable to find distributor: {invoice_dict['distributor']}, Skipping")

    def update_or_create_invoice_item(self, distributor, invoice_model, invoice_item_dict):
        invoice_item, created = self.create_invoice_item(distributor, invoice_model, invoice_item_dict)
        if not created:
            return self._update_invoice_item(invoice_item, invoice_item_dict)
        return invoice_item

    def _update_invoice_item(self, current_invoice_item, invoice_item_dict):
        updated = False
        for field in ['order_number', 'distributor_order_number']:
            current_attr = getattr(current_invoice_item, field)
            #new_attr = getattr(new_invoice_item, field)
            #if current_attr != new_attr and new_attr is not None and current_attr is None:
            #    updated = True
            #    setattr(current_invoice_item, field, new_attr)
        #if updated:
        #    current_invoice_item.save()
        return current_invoice_item

    def create_invoice_item(self, distributor, invoice_model, invoice_item_dict):
        position = invoice_item_dict
        logger.debug('creating invoice item: %s', position)
        distributor_order_number, created = DistributorOrderNumber.objects.get_or_create(
            distributor=distributor,
            don=position['distributor_number']
        )

        if created:
            self.DON_to_update.append(distributor_order_number)

        net_price = decimal.Decimal(position['price']['net']) if position['price']['net'] else None
        tax = position['price']['vat_tax']
        gross_price = None
        if 'gross' in position['price'] and position['price']['gross']:
            gross_price = decimal.Decimal(position['price']['gross'])
        elif tax and net_price:
            gross_price = net_price * decimal.Decimal(tax) / 100
        invoice_item, created = InvoiceItem.objects.get_or_create(
            invoice=invoice_model,
            position_in_invoice=int(position['position']),
            defaults={
                "order_number": position['order_number'] if 'order_number' in position else None,
                "distributor_order_number": distributor_order_number,
                "ordered_quantity": position['ordered_quantity'],
                "shipped_quantity": position['shipped_quantity'],
                "price_net": net_price,
                "price_gross": gross_price,
                "price_vat_tax": tax,
                "price_currency": Currency[position['price']['currency_display']]
            })
        return invoice_item, created
