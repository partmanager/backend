import logging
from celery import shared_task
from .models import DistributorOrderNumber, ManufacturerOrderNumber, get_manufacturer_by_name

logger = logging.getLogger('distributors')


@shared_task
def update_manufacturer_order_number():
    logger.debug('updating distributor order numbers')

    don_to_update = DistributorOrderNumber.objects.filter(manufacturer_order_number__isnull=True)

    last_manufacturer_name = None
    manufacturer_obj = None
    for don in don_to_update:
        logger.info(f'Updating {don}')

        manufacturer_name_converted = don.distributor.convert_manufacturer_name(don.manufacturer_name_text)
        logger.debug(f"\tDistributor manufacturer name: {don.manufacturer_name_text}, converted manufacturer name: {manufacturer_name_converted}")
        if last_manufacturer_name != manufacturer_name_converted:
            new_manufacturer = get_manufacturer_by_name(manufacturer_name_converted)
            if new_manufacturer:
                last_manufacturer_name = manufacturer_name_converted
                manufacturer_obj = new_manufacturer
            else:
                logger.warning(f"\tManufacturer {manufacturer_name_converted} don't exist")
                last_manufacturer_name = None
                manufacturer_obj = None

        if manufacturer_obj is not None:
            logger.debug(f"\tManufacturer: {manufacturer_obj}")

            order_number = don.manufacturer_order_number_text if don.manufacturer_order_number_text else don.distributor_order_number_text
            logger.debug(f"\tsearching for MON with order number: {order_number}")
            try:
                mon = ManufacturerOrderNumber.objects.get(
                    manufacturer_order_number__iexact=order_number,
                    manufacturer=manufacturer_obj)
                don.manufacturer_order_number = mon
                don.save()
                logger.info("\tSuccess")
            except ManufacturerOrderNumber.DoesNotExist as e:
                logger.info(f"\tUnable to update: {e}")
