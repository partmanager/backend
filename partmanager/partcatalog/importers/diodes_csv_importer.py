import decimal

from partcatalog.models.diode import Diode
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_voltage_parameter, decode_current_parameter, decode_capacitance_parameter


def get_diode(manufacturer, part_number):
    part = Diode.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def decode_forward_voltage(dictionary):
    forward_voltage = {}
    index = 1

    if dictionary['Forward Voltage @ IF']:
        forward_voltage_str = dictionary['Forward Voltage @ IF'].split('@')
        print(forward_voltage_str)
        conditions = forward_voltage_str[1].split(',')
        fv = decode_voltage_parameter(forward_voltage_str[0])
        forward_voltage['forward_voltage1_max'] = fv['max']
        forward_voltage['forward_voltage1_at_forward_current'] = decode_current_parameter(conditions[0].replace('IF=', ''))['typ']
        forward_voltage['forward_voltage1_at_junction_temp'] = decimal.Decimal(conditions[1].replace('Tj=', ''))
        index = index + 1

    for field in dictionary:
        if 'Forward Voltage @ IF=' in field and dictionary[field]:
            at_forward_current = decode_current_parameter(field.replace('Forward Voltage @ IF=', ''))['typ']
            forward_voltage_str_list = dictionary[field].split('|')
            for forward_voltage_str in forward_voltage_str_list:
                forward_voltage_and_junction_temp = forward_voltage_str.split('@')
                print(forward_voltage_and_junction_temp)
                forward_voltage['forward_voltage{}_max'.format(index)] = \
                    decode_voltage_parameter(forward_voltage_and_junction_temp[0])['max']
                forward_voltage['forward_voltage{}_at_junction_temp'.format(index)] = decimal.Decimal(
                    forward_voltage_and_junction_temp[1].replace('Tj=', ''))
                forward_voltage['forward_voltage{}_at_forward_current'.format(index)] = at_forward_current
                index = index + 1
    print("Forward Voltage:", forward_voltage)
    return forward_voltage


def decode_peak_forward_surge_current(dictionary):
    ifsm_str_list = dictionary['IFSM'].split('|')
    for ifsm_str in ifsm_str_list:
        current_and_duration = ifsm_str.split('@')
        return decode_current_parameter(current_and_duration[0])['typ']


def decode_recovery_time(dictionary):
    if dictionary['trr']:
        if 'max' in dictionary['trr']:
            return {'reverse_recovery_time_in_ns': decimal.Decimal(dictionary['trr'].replace('max', '').replace('ns', ''))}
        else:
            return {'reverse_recovery_time_in_ns': decimal.Decimal(dictionary['trr'].replace('ns', ''))}
    else:
        return {}


def decode_reverse_current(dictionary):
    reverse_current = {}
    index = 1
    for field in dictionary:
        if 'Reverse Current @ VR=' in field and dictionary[field]:
            at_reverse_voltage = decimal.Decimal(field.replace('Reverse Current @ VR=', '').replace('V', ''))
            reverse_current_str_list = dictionary[field].split('|')
            for reverse_current_str in reverse_current_str_list:
                current_and_junction_temp = reverse_current_str.split('@')
                # print(current_and_junction_temp)
                reverse_current['reverse_current{}_max'.format(index)] = \
                    decode_current_parameter(current_and_junction_temp[0])['max']
                reverse_current['reverse_current{}_at_junction_temp'.format(index)] = decimal.Decimal(
                    current_and_junction_temp[1].replace('Tj=', ''))
                reverse_current['reverse_current{}_at_reverse_voltage'.format(index)] = at_reverse_voltage
                index = index + 1
    print("Reverse Current:", reverse_current)
    return reverse_current


def decode_junction_capacitance(dictionary):
    if dictionary['Cd@1MHz']:
        capacitance_and_vr = dictionary['Cd@1MHz'].split('@')
        capacitance = decode_capacitance_parameter(capacitance_and_vr[0])
        vr = decode_voltage_parameter(capacitance_and_vr[1].replace('VR=', ''))
        print(capacitance_and_vr, capacitance, vr)
        junction_capacitance = {'capacitance_in_pf_at_frequency': 1000000,
                                'capacitance_in_pf_at_reverse_voltage': vr['typ']}
        if capacitance['max']:
            capacitance['max'] = capacitance['max'] * decimal.Decimal('1e12')
            junction_capacitance['capacitance_in_pf_max'] = capacitance['max']
        if capacitance['typ']:
            capacitance['typ'] = capacitance['typ'] * decimal.Decimal('1e12')
            junction_capacitance['capacitance_in_pf_typ'] = capacitance['typ']

        print("Junction Capacitance:", junction_capacitance)
        return junction_capacitance
    return {}


def create_diode(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package Type'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)
    forward_voltage = decode_forward_voltage(dictionary)
    recovery_time = decode_recovery_time(dictionary)
    reverse_current = decode_reverse_current(dictionary)
    junction_capacitance = decode_junction_capacitance(dictionary)
    part = Diode(manufacturer_part_number=part_number,
                 manufacturer=manufacturer,
                 package=package,
                 **common_parameters,
                 # Diode specific fields
                 forward_continuous_current=decode_current_parameter(dictionary['IF'])['typ'],
                 repetitive_peak_forward_current=decode_current_parameter(dictionary['IFRM'])['typ'],
                 peak_forward_surge_current=decode_peak_forward_surge_current(dictionary),
                 repetitive_peak_reverse_voltage=decimal.Decimal(dictionary['VRRM'].replace('V', '')),
                 power_rating=decimal.Decimal(dictionary['Power Rating'].replace('mW', '')) / 1000 if dictionary[
                     'Power Rating'] else None,
                 **junction_capacitance,
                 **forward_voltage,
                 **recovery_time,
                 **reverse_current
                 )
    part.description = part.generate_description()
    return part


def add_diode(dictionary):
    # print(dictionary)
    manufacturer_name = dictionary['Manufacturer']
    manufacturer = get_manufacturer_by_name(manufacturer_name)
    if manufacturer:
        part_number = dictionary['Part Number']
        part = get_diode(manufacturer, part_number)
        if not part:
            part = create_diode(manufacturer, part_number, dictionary)
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
            add_diode(row)
