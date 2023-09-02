import logging
from celery import shared_task
from .models import InventoryPosition

logger = logging.getLogger('inventory')


@shared_task
def update_inventory_mpn_assignments():
    logger.info('Updating inventory MPNs')

    inventory_position_to_update = InventoryPosition.objects.filter(part__isnull=True,
                                                                    invoice__distributor_order_number__isnull=False)

    for ip in inventory_position_to_update:
        part = ip.invoice.distributor_order_number.manufacturer_order_number
        if part is not None:
            logger.debug(f'{ip} ===> {part}')
            if ip.manufacturer is None or part.manufacturer == ip.manufacturer or ip.manufacturer.name == 'Unknown':
                ip.part = part
                ip.save()
                logger.debug("\tsaved")
