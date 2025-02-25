import logging
from celery import shared_task

from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from .models import InventoryPosition

logger = logging.getLogger('inventory')




@shared_task
def update_inventory_mpn_assignments():
    logger.info('Updating inventory MPNs')

    invoice_based_update()
    name_based_update()


def invoice_based_update():
    inventory_position_to_update = InventoryPosition.objects.filter(mon__isnull=True,
                                                                    invoice__distributor_order_number__isnull=False)

    for ip in inventory_position_to_update:
        mon = ip.invoice.distributor_order_number.manufacturer_order_number
        if mon is not None:
            logger.debug(f'{ip} ===> {mon}')
            if ip.manufacturer is None or mon.manufacturer == ip.manufacturer or ip.manufacturer.name == 'Unknown':
                ip.mon = mon
                ip.save()
                logger.debug("\tsaved")


def name_based_update():
    inventory_position_to_update = InventoryPosition.objects.filter(mon__isnull=True,
                                                                    invoice__distributor_order_number__isnull=True,
                                                                    manufacturer__isnull=False)

    for ip in inventory_position_to_update:
        if ip.manufacturer.name != 'Unknown':
            try:
                mon = ManufacturerOrderNumber.objects.get(manufacturer=ip.manufacturer,
                                                          manufacturer_order_number=ip.name)
                logger.debug(f'{ip} ===> {mon}')
                ip.mon = mon
                ip.save()
            except ManufacturerOrderNumber.DoesNotExist as e:
                logger.debug(e)
