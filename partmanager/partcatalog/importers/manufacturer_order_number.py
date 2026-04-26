import logging
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.models.packaging import Packaging


logger = logging.getLogger('partcatalog')


def add_manufacturer_order_numbers(dry_run, manufacturer, part, order_numbers):
    for order_number in order_numbers:
        try:
            packaging = decode_packaging(order_numbers[order_number])
            logger.debug(f'Updating MON: {order_number} for part {part.MPN}')
            if not dry_run:
                ManufacturerOrderNumber.objects.update_or_create(
                    MON=order_number,
                    manufacturer=manufacturer,
                    defaults={
                        "packaging": packaging,
                        "part": part}
                )
        except Exception as e:
            logger.error(f"Exception {e}")


def decode_packaging(packaging_json):
    packaging = Packaging()
    packaging.code = None
    packaging.type = 'u'
    packaging.quantity = None
    packaging.packaging_data = None
    if packaging_json:
        packaging.code = packaging_json['code'] if 'code' in packaging_json else None
        packaging.type = packaging_json['type'] if 'type' in packaging_json else 'u'
        packaging.quantity = packaging_json['qty'] if 'qty' in packaging_json else None
        if packaging.type in ["Paper Tape / Reel", "Embossed Tape / Reel"] and 'packagingData' in packaging_json:
            packaging.packaging_data = decode_tape_reel_packaging(packaging_json)
    return packaging

def decode_tape_reel_packaging(packaging_json):
    return packaging_json['packagingData'] if packaging_json['packagingData'] else None