import logging
import json
import os
from django.db.utils import ProgrammingError
from distributors.models import Distributor, DistributorManufacturer, DistributorOrderNumber
from manufacturers.models import get_manufacturer_by_name

logger = logging.getLogger('distributors')


def import_distributor_manufacturer_translation(distributor, manufacturer_name_translation):
    for name_translation in manufacturer_name_translation:
        logger.info(
            f"Creating Distributor manufacturer name conversion for {name_translation['distributor_manufacturer_name']} => {name_translation['manufacturer_name']}")
        manufacturer = get_manufacturer_by_name(name_translation['manufacturer_name'])
        if manufacturer:
            dist_manufacturer, created = DistributorManufacturer.objects.get_or_create(
                distributor=distributor,
                manufacturer_name_text=name_translation['distributor_manufacturer_name'],
                defaults={"manufacturer": manufacturer})
            if not created:
                logger.warning(
                    "Manufacturer name conversion exists. Unimplemented manufacturer comparison during import")
        else:
            logger.warning("Unable to find manufacturer, skipping...")


def import_distributor_order_number(distributor, distributor_order_numbers):
    logger.info(f"Importing DON for {distributor}, DON count {len(distributor_order_numbers)}")
    skipped_don = 0
    added_don = 0
    for don in distributor_order_numbers:
        try:
            distributor_order_number, created = DistributorOrderNumber.objects.get_or_create(
                distributor=distributor,
                distributor_order_number_text=don['distributor_order_number'],
                manufacturer_order_number_text=don['manufacturer_order_number'],
                defaults={
                    'manufacturer_name_text': don['manufacturer_name'],
                    'part_url': don['part_url']
                })
            if created:
                logger.debug(f"Added {don['distributor_order_number']}")
                added_don += 1
                distributor_order_number.update_manufacturer_order_number()
                distributor_order_number.save()
            else:
                skipped_don += 1
                logger.debug(f"{don['distributor_order_number']} DON exists, skipping...")
        except ProgrammingError as e:
            logger.error(f"Exception: {repr(e)}, while importing DON: {don}")
    logger.info(f"Finished importing DON for {distributor}, added new DON {added_don}, "
                f"DON that already existed and was skipped: {skipped_don}")


def import_distributor_from_dict(distributor_dict):
    distributor, created = Distributor.objects.get_or_create(
        name=distributor_dict['name'],
        defaults={
            'website_url': distributor_dict['website'],
            'connector_data': distributor_dict['connector_data'] if 'connector_data' in distributor_dict else None
        })
    if created:
        logger.info(f"Created distributor {distributor}")

    import_distributor_manufacturer_translation(distributor, distributor_dict['manufacturer_name_translation'])
    import_distributor_order_number(distributor, distributor_dict['distributor_order_numbers'])


def process_distributor_file(distributor_filename):
    logger.info("Importing distributor", distributor_filename)
    with open(distributor_filename, 'r') as distributor_file:
        distributor = json.load(distributor_file)
        import_distributor_from_dict(distributor)


def import_distributor(workdir):
    for distributor_file in os.listdir(workdir):
        if distributor_file.endswith('.json'):
            process_distributor_file(workdir + '/' + distributor_file)
