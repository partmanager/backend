import decimal

from partcatalog.models.transistor_bipolar import TransistorBipolar
from manufacturers.models import get_manufacturer_by_name
import csv
from decimal import Decimal
from partcatalog.importers.common import str_to_production_status, add_manufacturer_order_number
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_inductance_parameter, decode_resistance_parameter, frequency_str_to_decimal, \
    resistance_str_to_decimal, voltage_str_to_decimal, current_str_to_decimal, power_str_to_decimal, \
    decode_integer_parameter, decode_frequency_parameter, decode_voltage_parameter, decode_current_parameter, decode_capacitance_parameter


def decode_voltage_field(dictionary, filed_name, result_field_name):
    for field in dictionary:
        if filed_name in field:
            at_temperature = field.replace(filed_name + ' @', '').strip()
            voltage_str = dictionary[field]
            return {result_field_name: voltage_str_to_decimal(voltage_str)}


def decode_current_field(dictionary, filed_name, result_field_name):
    for field in dictionary:
        if filed_name in field:
            at_temperature = field.replace(filed_name + ' @', '').strip()
            current_str = dictionary[field]
            return {result_field_name: current_str_to_decimal(current_str)}


def decode_power_field(dictionary, filed_name, result_field_name):
    for field in dictionary:
        if filed_name in field:
            at_temperature = field.replace(filed_name + ' @', '').strip()
            power_str = dictionary[field]
            return {result_field_name: power_str_to_decimal(power_str)}


def decode_collector_base_voltage(dictionary):
    return decode_voltage_field(dictionary, 'V_CBO', 'collector_base_voltage')


def decode_collector_emitter_voltage(dictionary):
    return decode_voltage_field(dictionary, 'V_CEO', 'collector_emitter_voltage')


def decode_emitter_base_voltage(dictionary):
    return decode_voltage_field(dictionary, 'V_EBO', 'emitter_base_voltage')


def decode_collector_current(dictionary):
    return decode_current_field(dictionary, 'I_C', 'collector_current')


def decode_peak_collector_current(dictionary):
    return decode_current_field(dictionary, 'I_CM', 'peak_collector_current')


def decode_peak_base_current(dictionary):
    return decode_current_field(dictionary, 'I_BM', 'peak_base_current')


def decode_power_dissipation(dictionary):
    return decode_power_field(dictionary, 'P_D', 'power_dissipation')


def decode_parameter(parameters_str, value_parser, condition_parsers):
    parameter_values = []
    if parameters_str:
        for parameter_str in parameters_str.split('|'):
            value_str, conditions_str = parameter_str.split('@')
            print(value_str, conditions_str)
            value_dict = {}
            value_dict.update(value_parser(value_str))
            for condition in conditions_str.split(','):
                for condition_parser in condition_parsers:
                    parsed_condition = condition_parser(condition)
                    if parsed_condition:
                        value_dict.update(parsed_condition)
            parameter_values.append(value_dict)
    return parameter_values


def decode_collector_current_condition(condition_str):
    if 'I_C' in condition_str:
        condition_str = condition_str.replace('I_C=', '')
        return {'at_collector_current': current_str_to_decimal(condition_str)}


def decode_base_current_condition(condition_str):
    if 'I_B' in condition_str:
        condition_str = condition_str.replace('I_B=', '')
        return {'at_base_current': current_str_to_decimal(condition_str)}


def decode_collector_emitter_voltage_condition(condition_str):
    if 'V_CE' in condition_str:
        condition_str = condition_str.replace('V_CE=', '')
        return {'at_collector_emitter_voltage': voltage_str_to_decimal(condition_str)}


def decode_collector_base_voltage_condition(condition_str):
    if 'V_CB' in condition_str:
        condition_str = condition_str.replace('V_CB=', '')
        return {'at_collector_base_voltage': voltage_str_to_decimal(condition_str)}


def decode_emitter_base_voltage_condition(condition_str):
    if 'V_EB' in condition_str:
        condition_str = condition_str.replace('V_EB=', '')
        return {'at_voltage': voltage_str_to_decimal(condition_str)}


def decode_frequency_condition(condition_str):
    if 'f' in condition_str:
        condition_str = condition_str.replace('f=', '')
        return {'at_frequency': frequency_str_to_decimal(condition_str)}


def decode_collector_base_breakdown_voltage(dictionary):
    out_dict = decode_parameter(dictionary['BV_CBO @ T_A=25'], decode_voltage_parameter,
                                [decode_collector_current_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'collector_base_breakdown_voltage_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_collector_emitter_breakdown_voltage(dictionary):
    out_dict = decode_parameter(dictionary['BV_CEO @ T_A=25'], decode_voltage_parameter,
                                [decode_collector_current_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'collector_emitter_breakdown_voltage_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_emitter_base_breakdown_voltage(dictionary):
    out_dict = decode_parameter(dictionary['BV_EBO @ T_A=25'], decode_voltage_parameter,
                                [decode_collector_current_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'emitter_base_breakdown_voltage_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_collector_emitter_cut_off_current(dictionary):
    out_dict = decode_parameter(dictionary['I_CES @ T_A=25'], decode_current_parameter,
                                [decode_collector_emitter_voltage_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'collector_emitter_cut_off_current1_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_emitter_base_cut_off_current(dictionary):
    out_dict = decode_parameter(dictionary['I_EBO @ T_A=25'], decode_current_parameter,
                                [decode_emitter_base_voltage_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'emitter_base_cut_off_current_' + k: v for k, v in out_dict[0].items()}
        return result
    return {}


def decode_dc_current_gain(dictionary):
    out_dict = decode_parameter(dictionary['h_FE @ T_A=25'], decode_integer_parameter,
                                [decode_collector_emitter_voltage_condition, decode_collector_current_condition])
    if 0 < len(out_dict) <= 2:
        result = {}
        for index in range(len(out_dict)):
            out_dict[index]['at_temp'] = 25
            result.update({'dc_current_gain{}_'.format(index + 1) + k: v for k, v in out_dict[index].items()})
        print(result)
        return result


def decode_collector_emitter_saturation_voltage(dictionary):
    out_dict = decode_parameter(dictionary['V_CE(SAT) @ T_A=25'], decode_voltage_parameter,
                                [decode_collector_current_condition, decode_base_current_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'collector_emitter_saturation_voltage_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_base_emitter_voltage(dictionary):
    out_dict = decode_parameter(dictionary['V_BE @ T_A=25'], decode_voltage_parameter,
                                [decode_collector_current_condition, decode_collector_emitter_voltage_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'base_emitter_voltage_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_gain_bandwidth_product(dictionary):
    out_dict = decode_parameter(dictionary['f_T @ T_A=25'], decode_frequency_parameter,
                                [decode_collector_emitter_voltage_condition, decode_collector_current_condition,
                                 decode_frequency_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'gain_bandwidth_product_' + k: v for k, v in out_dict[0].items()}
        return result


def decode_collector_base_capacitance(dictionary):
    out_dict = decode_parameter(dictionary['C_CBO @ T_A=25'], decode_capacitance_parameter,
                                [decode_collector_base_voltage_condition,
                                 decode_frequency_condition])
    if len(out_dict) == 1:
        out_dict[0]['at_temp'] = 25
        result = {'collector_base_capacitance_' + k: v for k, v in out_dict[0].items()}
        return result


def get_part(manufacturer, part_number):
    part = TransistorBipolar.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
    if len(part) > 0:
        if len(part) == 1:
            return part[0]
        else:
            print("**********************************")


def create_part(manufacturer, part_number, dictionary):
    package = part_dict_to_package(dictionary['Package Type'], dictionary)
    common_parameters = decode_common_part_parameters(dictionary)

    part = TransistorBipolar(manufacturer_part_number=part_number,
                             manufacturer=manufacturer,
                             package=package,
                             **common_parameters,
                             # Bipolar Transistor specific fields
                             # **decode_collector_base_voltage(dictionary),
                             **decode_collector_emitter_voltage(dictionary),
                             # **decode_emitter_base_voltage(dictionary),
                             **decode_collector_current(dictionary),
                             # **decode_peak_collector_current(dictionary),
                             # **decode_peak_base_current(dictionary),
                             # **decode_power_dissipation(dictionary),
                             # **decode_collector_base_breakdown_voltage(dictionary),
                             # **decode_collector_emitter_breakdown_voltage(dictionary),
                             # **decode_emitter_base_breakdown_voltage(dictionary),
                             # **decode_collector_emitter_cut_off_current(dictionary),
                             **decode_emitter_base_cut_off_current(dictionary),
                             # **decode_dc_current_gain(dictionary),
                             # **decode_collector_emitter_saturation_voltage(dictionary),
                             # **decode_base_emitter_voltage(dictionary),
                             # **decode_gain_bandwidth_product(dictionary),
                             # **decode_collector_base_capacitance(dictionary)
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
        print(f"Unknown manufacturer: {manufacturer_name}")


def parts_import(filename):
    print("Importing Bipolar Transistors from csv file")
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='unix')
        for row in csvreader:
            add_part(row)
