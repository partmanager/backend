import decimal

from partcatalog.models.diode import TVS
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number, \
    decode_common_part_parameters
from partcatalog.importers.package_importer import part_dict_to_package
from .parameter_decoder import decode_parameter, decode_voltage_parameter, decode_current_parameter, \
    current_str_to_decimal, voltage_str_to_decimal, decode_power_parameter


def decode_reverse_current_condition(condition_str):
    if 'I_R=' in condition_str:
        condition_str = condition_str.replace('I_R=', '')
        return {'at_reverse_current': current_str_to_decimal(condition_str)}


def decode_peak_current_condition(condition_str):
    if 'I_PP=' in condition_str:
        condition_str = condition_str.replace('I_PP=', '')
        return {'at_peak_current': current_str_to_decimal(condition_str)}


def decode_reverse_standoff_voltage_condition(condition_str):
    if 'V_RWM=' in condition_str:
        condition_str = condition_str.replace('V_RWM=', '')
        return {'at_reverse_standoff_voltage': voltage_str_to_decimal(condition_str)}


def decode_pulse_time_condition(condition_str):
    if 'tp=' in condition_str:
        condition_str = condition_str.replace('tp=', '')


def decode_breakdown_voltage(dictionary):
    breakdown_voltage = decode_parameter(dictionary['Breakdown  Voltage (V_BR)'], decode_voltage_parameter,
                                         [decode_reverse_current_condition])
    if len(breakdown_voltage) == 1:
        return {'breakdown_voltage_min': breakdown_voltage[0]['min'],
                'breakdown_voltage_typ': breakdown_voltage[0]['typ'],
                'breakdown_voltage_max': breakdown_voltage[0]['max'],
                'breakdown_voltage_at_reverse_current_uA': breakdown_voltage[0]['at_reverse_current'] * 1000000}


def decode_clamping_voltage(dictionary):
    clamping_voltages = decode_parameter(dictionary['Clamping  Voltage (V_CL) @ T_A=25℃'], decode_voltage_parameter,
                                         [decode_peak_current_condition])
    print("\tDecoded clamping voltage:", clamping_voltages)
    for i, clamping_voltage in enumerate(clamping_voltages):
        assert (clamping_voltage['min'] is None)
        assert (clamping_voltage['typ'] is None)
        index = i + 1 if i + 1 != 1 else ''
        return {'clamping_voltage{}_max'.format(index): clamping_voltage['max'],
                'clamping_voltage{}_at_peak_current'.format(index): clamping_voltage['at_peak_current'] if 'at_peak_current' in clamping_voltage else None}


def decode_reverse_leakage_current(dictionary):
    leakage_currents = decode_parameter(dictionary['Reverse Leakage Current (I_RM) @ T_A=25℃'],
                                        decode_current_parameter,
                                        [decode_reverse_standoff_voltage_condition])
    print("\tDecoded reverse leakage current:", leakage_currents)
    return {'reverse_leakage_current_max_in_uA': leakage_currents[0]['max'] * 1000000 if leakage_currents[0]['max'] else None}


def decode_power_rating(dictionary):
    power_rating = decode_parameter(dictionary['Power Rating'],
                                    decode_power_parameter,
                                    [decode_pulse_time_condition])
    print("\tDecoded Power Rating:", power_rating)
    if power_rating:
        return {'power_rating_in_wats': power_rating[0]['max']}
    else:
        return {}


def decode_peak_pulse_current_max(dictionary):
    if dictionary['Peak Pulse Current (IPP)']:
        ipp = decimal.Decimal(dictionary['Peak Pulse Current (IPP)'].replace('A', '').replace('max.', ''))
        return {'peak_pulse_current_max_in_amper': ipp}
    else:
        return {}


def get_tvs(manufacturer, part_number):
    part = TVS.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_tvs(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)
    decode_power_rating(dictionary)
    part = TVS(manufacturer_part_number=part_number,
               manufacturer=manufacturer,
               package=package,
               **common_parameters,
               # TVS specyfic fields
               configuration=TVS.configuration_from_str(dictionary['Directions']),
               reverse_standoff_voltage_in_volts=decimal.Decimal(
                   dictionary['Reverse  Standoff  Voltage (V_RWM) @ T_A=25℃'].replace('V', '').replace('max.', '')),
               **decode_breakdown_voltage(dictionary),  # V_BR
               **decode_clamping_voltage(dictionary),  # V_CL
               **decode_reverse_leakage_current(dictionary),
               **decode_power_rating(dictionary),
               **decode_peak_pulse_current_max(dictionary)
               )
    part.description = part.generate_description()
    return part


def add_tvs(dictionary):
    # print(dictionary)
    manufacturer_name = dictionary['Manufacturer']
    manufacturer = get_manufacturer_by_name(manufacturer_name)
    if manufacturer:
        part_number = dictionary['Part Number']
        part = get_tvs(manufacturer, part_number)
        if not part:
            part = create_tvs(manufacturer, part_number, dictionary)
            part.save()
            print(part.manufacturer_part_number, "\tAdd")
        else:
            print(part.manufacturer_part_number, "\tSkip")
        add_manufacturer_order_number(manufacturer, part, dictionary)
    else:
        print("Unknown manufacturer")


def parts_import(filename):
    print("Importing TVS from csv file")
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='unix')
        for row in csvreader:
            add_tvs(row)
