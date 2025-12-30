import logging

from django.core.files import File
from invoices.models import  InvoiceAttachment


logger = logging.getLogger('invoices')


def get_or_create_invoice_attachment(invoice, invoice_attachment_dict, files_dir) -> InvoiceAttachment | None:
    try:
        attachment = InvoiceAttachment.objects.get(
            invoice=invoice,
            attachment=invoice_attachment_dict['attachment']['filename_org'] if invoice_attachment_dict['attachment'] else None,
            description=invoice_attachment_dict['description'],
            note=invoice_attachment_dict['note']
        )
        logger.info(
            f"Found attachment for invoice: {invoice.distributor.name}: {invoice.number}, Description: {invoice_attachment_dict['description']}")
        return attachment
    except InvoiceAttachment.DoesNotExist:
        logger.info(f"Creating attachment for invoice: {invoice.distributor.name}: {invoice.number}, Description: {invoice_attachment_dict['description']}")
        attachment = InvoiceAttachment(
            invoice=invoice,
            description=invoice_attachment_dict['description'],
            note=invoice_attachment_dict['note']
        )
        if 'attachment' in invoice_attachment_dict and invoice_attachment_dict['attachment']:
            f = open(files_dir.joinpath(invoice_attachment_dict['attachment']['filename']), mode='rb')
            django_file = File(f)
            attachment.attachment.save(invoice_attachment_dict['attachment']['filename_org'], django_file)
        attachment.save()
        return attachment
    except InvoiceAttachment.MultipleObjectsReturned:
        logger.error("Unable to create invoice attachment, multiple objects returned")