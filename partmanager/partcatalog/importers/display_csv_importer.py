import decimal

from partcatalog.models.display import Display
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_resistance_parameter, decode_current_parameter, decode_parameter, \
    decode_temperature_condition, decode_parameter_and_tolerance, decode_frequency_condition
from .units_decoder import decode_dc_resistance, decode_insulation_resistance, decode_dc_current


def decode_resolution(dictionary):
    if dictionary["Resolution"]:
        width, height = dictionary["Resolution"].split('x')
        return {'resolution_width': width, 'resolution_height': height}
    else:
        return {}


def decode_controller(dictionary):
    controller = {}
    if dictionary["Controller"]:
        manufacturer, part_number = dictionary["Controller"].split(',')
        controller['controller_manufacturer'] = manufacturer
        controller['controller_part_number'] = part_number
    if dictionary['Controller Interface']:
        controller["controller_interface"] = dictionary['Controller Interface']
    return controller


def get_part(manufacturer, part_number):
    part = Display.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_part(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package Type'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)

    part = Display(manufacturer_part_number=part_number,
                   manufacturer=manufacturer,
                   package=package,
                   **common_parameters,
                   # Display specific fields
                   color=dictionary['Color'],
                   **decode_resolution(dictionary),
                   **decode_controller(dictionary),
                   backlight_source=dictionary['Backlight'],
                   backlight_color=dictionary['Backlight Color'])
    part.description = part.generate_description()
    return part


def add_part(dictionary):
    # print(dictionary)
    manufacturer_name = dictionary['Manufacturer']
    manufacturer = get_manufacturer_by_name(manufacturer_name)
    if manufacturer:
        part_number = dictionary['Part Number']
        part = get_part(manufacturer, part_number)
        if not part:
            part = create_part(manufacturer, part_number, dictionary)
            part.save()
            print(part.manufacturer_part_number, "\tAdd")
        else:
            print(part.manufacturer_part_number, "\tSkip")
        add_manufacturer_order_number(manufacturer, part, dictionary)
    else:
        print("Unknown manufacturer")


def parts_import(filename):
    print("Importing Common mode chokes from csv file")
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='unix')
        for row in csvreader:
            add_part(row)
