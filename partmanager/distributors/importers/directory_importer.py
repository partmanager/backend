import logging
import json
import os
from distributors.models import Distributor, DistributorManufacturer, DistributorOrderNumber
from manufacturers.models import get_manufacturer_by_name

logger = logging.getLogger('distributors')


def import_distributor_manufacturer_translation(distributor, manufacturer_name_translation):
    for name_translation in manufacturer_name_translation:
        logger.info(
            f"Creating Distributor manufacturer name conversion for {name_translation['distributor_manufacturer_name']} => {name_translation['manufacturer_name']}")
        manufacturer = get_manufacturer_by_name(name_translation['manufacturer_name'])
        if manufacturer:
            logger.debug("\t\tfound manufacturer")
            logger.debug(str(name_translation))
            distributor_manufacturer = DistributorManufacturer(distributor=distributor,
                                                               manufacturer_name_text=name_translation[
                                                                   'distributor_manufacturer_name'],
                                                               manufacturer=manufacturer)
            logger.debug(str(distributor_manufacturer))
            distributor_manufacturer.save()
            logger.info("\tSaved")
        else:
            print("Unable to find manufacturer, skipping...")


def import_distributor_order_number(distributor, distributor_order_numbers):
    for don in distributor_order_numbers:
        distributor_order_number, created = DistributorOrderNumber.objects.get_or_create(
            distributor=distributor,
            distributor_order_number_text=don['distributor_order_number'],
            manufacturer_order_number_text=don['manufacturer_order_number'],
            defaults={
                'manufacturer_name_text': don['manufacturer_name'],
                'part_url': don['part_url']
            })
        if created:
            distributor_order_number.update_manufacturer_order_number()
            distributor_order_number.save()
        else:
            print("Distributor order number exists, skipping...")


def import_distributor_from_dict(distributor_dict):
    distributor, created = Distributor.objects.get_or_create(
        name=distributor_dict['name'],
        defaults={
            'website_url': distributor_dict['website'],
            'connector_data': distributor_dict['connector_data'] if 'connector_data' in distributor_dict else None
        })
    if created:
        import_distributor_manufacturer_translation(distributor, distributor_dict['manufacturer_name_translation'])
        import_distributor_order_number(distributor, distributor_dict['distributor_order_numbers'])
    else:
        print("Distributor exist, skipping...")


def __process_distributor_file(distributor_filename):
    print("Importing distributor", distributor_filename)
    with open(distributor_filename, 'r') as invoice_file:
        distributor = json.load(invoice_file)
        import_distributor_from_dict(distributor)


def import_distributor(workdir):
    for distributor_file in os.listdir(workdir):
        if distributor_file.endswith('.json'):
            __process_distributor_file(workdir + '/' + distributor_file)
