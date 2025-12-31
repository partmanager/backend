import decimal
import logging

from django.core.files import File
from invoices.models import  PaymentConfirmation
from partmanager.choices import Currency, PaymentMethod

logger = logging.getLogger('invoices')

payment_method_map = {
    'Bank transfer': PaymentMethod.BANK_TRANSFER,
    'Cash': PaymentMethod.CASH,
    'Credit card': PaymentMethod.CREDIT_CARD,
    'PayPal': PaymentMethod.PAY_PAL
}

def create_payment_confirmation(invoice, payment_confirmation_dict, files_dir) -> PaymentConfirmation:
    logger.debug('creating paymentConfirmation for invoice: %s', str(invoice))
    value = decimal.Decimal(
        payment_confirmation_dict['value']['net']) if payment_confirmation_dict['value']['net'] else None
    payment_confirmation, created = PaymentConfirmation.objects.update_or_create(
        invoice=invoice,
        payment_date=payment_confirmation_dict['payment_date'],
        value_net=value,
        value_currency=Currency[payment_confirmation_dict['value']['currency_display']],
        payment_method=payment_method_map[payment_confirmation_dict['method']],
        note=payment_confirmation_dict['note'],
        defaults={}
    )
    if 'file' in payment_confirmation_dict and payment_confirmation_dict['file']:
        logger.debug('Adding confirmation file into payment confirmation: %s', str(payment_confirmation))
        f = open(files_dir.joinpath(payment_confirmation_dict['file']['filename']), mode='rb')
        django_file = File(f)
        payment_confirmation.confirmation_file.save(payment_confirmation_dict['file']['filename'], django_file)
    return payment_confirmation
