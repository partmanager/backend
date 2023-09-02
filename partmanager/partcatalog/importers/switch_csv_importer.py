import decimal

from partcatalog.models.switch import Switch
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_resistance_parameter, decode_current_parameter, decode_parameter, \
    decode_temperature_condition, decode_parameter_and_tolerance, decode_frequency_condition
from .units_decoder import decode_dc_resistance, decode_insulation_resistance, decode_dc_current


def get_part(manufacturer, part_number):
    part = Switch.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_part(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package Type'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)

    part = Switch(manufacturer_part_number=part_number,
                  manufacturer=manufacturer,
                  package=package,
                  **common_parameters,
                  # Switch specific fields
                  switch_type=Switch.SwitchType.from_string(dictionary['Switch Type']),
                  configuration=Switch.ConfigurationChoices.from_string(dictionary['Configuration']) if dictionary['Configuration'] else None,
                  position_count=int(dictionary['Position Count']),
                  pin_pitch=decimal.Decimal(dictionary["Pin Pitch"].replace('mm', '')) if dictionary["Pin Pitch"] else None,
                  max_switching_voltage=decimal.Decimal(dictionary["Switching Voltage"].replace('V', '')) if dictionary["Switching Voltage"] else None,
                  **decode_dc_current(dictionary['Switching Current'], 'switching_current'),
                  **decode_dc_resistance(dictionary['Contact Resistance'], 'contact_resistance'),
                  **decode_insulation_resistance(dictionary['Insulation Resistance'], 'insulation_resistance'),
                  operating_life=int(dictionary['Operating Life']) if dictionary['Operating Life'] else None
                  )
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
