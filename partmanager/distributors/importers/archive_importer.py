import json
import time
import os
import shutil
from distributors.models import Distributor, DistributorManufacturer, DistributorOrderNumber
from manufacturers.models import get_manufacturer_by_name


def import_distributor_manufacturer_translation(distributor, manufacturer_name_translation):
    for name_translation in manufacturer_name_translation:
        manufacturer = get_manufacturer_by_name(name_translation['manufacturer_name'])
        if manufacturer:
            distributor_manufacturer = DistributorManufacturer(distributor=distributor,
                                                               manufacturer_name_text=name_translation[
                                                                   'distributor_manufacturer_name'],
                                                               manufacturer=manufacturer)
            distributor_manufacturer.save()
        else:
            print("Unable to find manufacturer, skipping...")


def import_distributor_order_number(distributor, distributor_order_numbers):
    for don in distributor_order_numbers:
        distributor_order_number = DistributorOrderNumber.objects.filter(distributor=distributor,
                                                                         distributor_order_number_text=don[
                                                                             'distributor_order_number'],
                                                                         manufacturer_order_number_text=don[
                                                                             'manufacturer_order_number'])
        if distributor_order_number:
            print("Distributor order number exists, skipping...")
        else:
            distributor_order_number = DistributorOrderNumber(distributor=distributor,
                                                              distributor_order_number_text=don[
                                                                  'distributor_order_number'],
                                                              manufacturer_order_number_text=don[
                                                                  'manufacturer_order_number'],
                                                              manufacturer_name_text=don['manufacturer_name'],
                                                              part_url=don['part_url'])
            distributor_order_number.update_manufacturer_order_number()
            distributor_order_number.save()


def import_distributor_from_dict(distributor_dict):
    distributor = Distributor.objects.filter(name=distributor_dict['name'])
    if distributor:
        print("Distributor exist, skipping...")
    else:
        distributor = Distributor(name=distributor_dict['name'],
                                  website_url=distributor_dict['website'],
                                  connector_data=distributor_dict['connector_data'])
        distributor.save()
        import_distributor_manufacturer_translation(distributor, distributor_dict['manufacturer_name_translation'])
        import_distributor_order_number(distributor, distributor_dict['distributor_order_numbers'])


def __process_distributor_file(distributor_filename):
    print("Importing distributor", distributor_filename)
    with open(distributor_filename, 'r') as invoice_file:
        distributor = json.load(invoice_file)
        import_distributor_from_dict(distributor)


def import_distributor(archive_file):
    workdir = '/tmp/distributor/import/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    archive_filename = workdir + '/' + archive_file.name
    with open(archive_filename, 'wb') as file:
        file.write(archive_file.read())
    shutil.unpack_archive(archive_filename, extract_dir=workdir)
    for distributor_file in os.listdir(workdir):
        if distributor_file.endswith('.json'):
            __process_distributor_file(workdir + '/' + distributor_file)
