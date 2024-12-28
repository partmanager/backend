import json
from django.db.models import Q
from manufacturers.models import Manufacturer


def add_or_update_manufacturer(manufacturer):
    filter = Q()
    if manufacturer['name'] is not None and len(manufacturer['name']) > 0:
        filter |= Q(name__iexact=manufacturer['name'])
    if manufacturer['full_name'] is not None and len(manufacturer['full_name']) > 0:
        filter |= Q(full_name__iexact=manufacturer['full_name'])
    manufacturer_list = Manufacturer.objects.filter(filter)
    if manufacturer_list:
        manufacturer_dict = manufacturer_list[0].to_dict()
        to_update = {}
        for key in manufacturer_dict:
            if key in manufacturer and manufacturer[key] is not None and manufacturer[key] != "":
                if manufacturer_dict[key] != manufacturer[key]:
                    if manufacturer_dict[key] is None:
                        to_update[key] = manufacturer[key]
                    elif manufacturer_dict[key] is not None and manufacturer[key] is not None:
                        print("error", manufacturer_dict[key], manufacturer[key])
        # for update in to_update:
        #     setattr(manufacturer_list[0], update, to_update[update])
        if to_update == {}:
            print("Manufacturer exist, nothing to do", manufacturer_list)
    else:
        full_name = manufacturer['full_name'] if manufacturer['full_name'] is not None and len(manufacturer['full_name']) > 0 else None
        manufacturer = Manufacturer(name=manufacturer['name'],
                                    full_name=full_name,
                                    address=manufacturer['address'],
                                    website=manufacturer['website'],
                                    email=manufacturer['email'],
                                    phone=manufacturer['phone'],
                                    comment=manufacturer['comment'])
        manufacturer.save()


def __process_manufacturers_file(manufacturers_filename):
    print("Importing manufacturers from file...", manufacturers_filename)
    with open(manufacturers_filename, 'r') as manufacturers_file:
        manufacturers = json.load(manufacturers_file)
        for manufacturer in manufacturers:
            add_or_update_manufacturer(manufacturer)
    print("Importing manufacturers from file... Done")


def import_manufacturers(workdir):
    __process_manufacturers_file(workdir.joinpath('manufacturers.json'))
