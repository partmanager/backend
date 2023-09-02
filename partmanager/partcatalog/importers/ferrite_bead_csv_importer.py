import decimal

from partcatalog.models.ferrite_bead import FerriteBead
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_inductance_parameter, decode_resistance_parameter, frequency_str_to_decimal, \
    resistance_str_to_decimal, decode_voltage_parameter, decode_current_parameter, decode_capacitance_parameter, \
    decode_parameter, decode_temperature_condition, decode_parameter_and_tolerance, decode_frequency_condition


def decode_tolerance(tolerance_str):
    if '±' in tolerance_str:
        tolerance_str = tolerance_str.replace('±', '').replace('%', '')
        tolerance = decimal.Decimal(tolerance_str)
        return {'over': tolerance, 'under': tolerance * -1, 'type': '%'}


def decode_impedance_and_tolerance(dictionary):
    impedance_tolerance_list = decode_parameter_and_tolerance(dictionary['Impedance'], decode_resistance_parameter, [decode_frequency_condition])
    impedance = {}
    index = 1
    for impedance_tolerance in impedance_tolerance_list:
        at_frequency = impedance_tolerance['at_frequency']
        tolerance = impedance_tolerance['tolerance']
        impedance_typ = impedance_tolerance['value']
        print(impedance_typ, tolerance)
        if tolerance is None:
            impedance.update({'impedance{}_typ'.format(index): impedance_typ,
                              'impedance{}_at_frequency'.format(index): at_frequency
                              })
            index = index + 1
        elif tolerance['type'] == '%':
            impedance_max = impedance_typ + impedance_typ * tolerance['under'] / 100
            impedance_min = impedance_typ + impedance_typ * tolerance['over'] / 100
            impedance.update({'impedance{}_min'.format(index): impedance_max,
                              'impedance{}_typ'.format(index): impedance_typ,
                              'impedance{}_max'.format(index): impedance_min,
                              'impedance{}_at_frequency'.format(index): at_frequency,
                              'impedance{}_tolerance'.format(index): tolerance['over']
                              })
            index = index + 1
    return impedance


def decode_dc_resistance(dictionary):
    dc_resistance_str = dictionary['DC Resistance']
    if dc_resistance_str:
        resistance = decode_resistance_parameter(dc_resistance_str)
        return {'dc_resistance_typ': resistance['typ'],
                'dc_resistance_max': resistance['max']}


def decode_dc_rated_current(dictionary):
    rated_current_list = decode_parameter(dictionary['Rated Current'], decode_current_parameter,
                                          [decode_temperature_condition])
    rated_current_dict = {}
    index = 1
    for rated_current in rated_current_list:
        rated_current_dict.update({
            'dc_rated_current{}_min'.format(index): rated_current['min'],
            'dc_rated_current{}_typ'.format(index): rated_current['typ'],
            'dc_rated_current{}_max'.format(index): rated_current['max'],
            'dc_rated_current{}_at_temp'.format(index): rated_current['at_temp']
        })
        index = index + 1
    return rated_current_dict


def get_part(manufacturer, part_number):
    part = FerriteBead.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_part(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package Type'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)

    impedance_and_tolerance = decode_impedance_and_tolerance(dictionary)
    dc_rated_current = decode_dc_rated_current(dictionary)
    dc_resistance = decode_dc_resistance(dictionary)
    part = FerriteBead(manufacturer_part_number=part_number,
                       manufacturer=manufacturer,
                       package=package,
                       **common_parameters,
                       # Inductor specific fields
                       **impedance_and_tolerance,
                       **dc_resistance,
                       **dc_rated_current
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
    print("Importing Diodes from csv file")
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='unix')
        for row in csvreader:
            add_part(row)
