from manufacturers.models import get_manufacturer_by_name
import csv
import decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from partcatalog.models.led import LED
from partcatalog.importers.common import *
from .common import decode_common_part_parameters
from .parameter_decoder import decode_voltage_parameter, decode_parameter


def get_led(manufacturer, part_number):
    part = LED.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_led(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package'], dictionary)
    #vf = str_to_voltage(dictionary['VF'])
    vf = decode_voltage_parameter(dictionary['VF'])#, decode_voltage_parameter, [])
    common_parameters = decode_common_part_parameters(dictionary)
    part = LED(manufacturer_part_number=part_number,
               manufacturer=manufacturer,
               package=package,
               **common_parameters,
               # LED specific fields
               continuous_forward_current_in_mA=decimal.Decimal(dictionary['IF continuous'].replace('mA', '')) if dictionary['IF continuous'] else None,
               peak_forward_current_in_mA=decimal.Decimal(dictionary['IF peak'].replace('mA', '')) if dictionary['IF peak'] else None,
               forward_voltage_min_in_volts=vf['min'],
               forward_voltage_typ_in_volts=vf['typ'],
               forward_voltage_max_in_volts=vf['max'],
               # forward_voltage_current_condition_in_mA = ,
               #luminous_intensity=dictionary['Luminous Intensity'],
               viewing_angle_in_deg=decimal.Decimal(dictionary['Viewing Angle']) if dictionary['Viewing Angle'] else None,
               reverse_voltage_max_in_volts=decimal.Decimal(dictionary['VR'].replace('V', '')) if dictionary['VR'] else None,
               color=LED.color_from_str(dictionary['Color'])
               )
    return part


def add_led(dictionary):
    # print(dictionary)
    manufacturer_name = dictionary['Manufacturer']
    manufacturer = get_manufacturer_by_name(manufacturer_name)
    if manufacturer:
        part_number = dictionary['Part Number']
        part = get_led(manufacturer, part_number)
        if not part:
            part = create_led(manufacturer, part_number, dictionary)
            part.save()
            print(part.manufacturer_part_number, "\tAdd")
        else:
            print(part.manufacturer_part_number, "\tSkip")
        add_manufacturer_order_number(manufacturer, part, dictionary)
    else:
        print("Unknown manufacturer")


def parts_import(filename):
    print("Importing LED from csv file")
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='unix')

        for row in csvreader:
            add_led(row)
