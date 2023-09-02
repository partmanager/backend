import math
import decimal


def default_debug(*kwargs):
    print(*kwargs)


def decode_parameter(parameters_str, value_parser, condition_parsers, log=default_debug):
    parameter_values = []
    if parameters_str:
        parameters = [x.strip() for x in parameters_str.split('|')]
        log("Decoding:", parameters)
        for parameter_str in parameters:
            log("Processing:", parameter_str)
            if '@' in parameter_str:
                value_str, conditions_str = parameter_str.split('@')
                value_str = value_str.strip()
                conditions_str = conditions_str.strip().split(',')
                log("\tpre parsed value:", value_str, "conditions:", conditions_str)
                value_parsed = value_parser(value_str)
                log("\tParsed value:", value_parsed)
                if value_parsed is None:
                    continue
                value_dict = value_parsed
                for condition in conditions_str:
                    log("\tParsing condition:", condition)
                    for condition_parser in condition_parsers:
                        parsed_condition = condition_parser(condition)
                        if parsed_condition:
                            log("\t\tParsed condition:", parsed_condition)
                            value_dict.update(parsed_condition)
                parameter_values.append(value_dict)
            else:
                value_dict = value_parser(parameter_str)
                parameter_values.append(value_dict)
    return parameter_values


def __process_parameter_and_tolerance(value_and_tolerance_str, value_parser):
    value_and_tolerance_str = value_and_tolerance_str.strip()
    if '%' in value_and_tolerance_str:
        value_str, tolerance_str = value_and_tolerance_str.strip().split(' ')
        print('value:', value_str, 'tolerance:', tolerance_str)
        value = value_parser(value_str)
        tolerance = decode_percent_parameter(tolerance_str)
        return {'value': value['typ'], 'tolerance': {'under': tolerance['min'],
                                                     'over': tolerance['max'],
                                                     'type': '%'}}
    else:
        if ' ' in value_and_tolerance_str:
            #value_str, tolerance_str = value_and_tolerance_str.split(' ')
            value = value_parser(value_and_tolerance_str)
            print(value)
            #tolerance = value_parser(tolerance_str)
            return {'value': value['typ'], 'tolerance': {'under': value['min'] - value['typ'] if value['min'] and value['typ'] else None,
                                                         'over': value['max'] - value['typ'] if value['typ'] else value['max'],
                                                         'type': ''}}
        else:
            value = value_parser(value_and_tolerance_str)
            return {'value': value['typ'], 'tolerance': None}


def decode_parameter_and_tolerance(parameters_str, value_parser, condition_parsers):
    parameter_values = []
    if parameters_str:
        for parameter_str in parameters_str.split('|'):
            if '@' in parameter_str:
                value_str, conditions_str = parameter_str.split('@')
                print(value_str, conditions_str)
                value_dict = __process_parameter_and_tolerance(value_str, value_parser)
                #value_dict.update(value_parser(value_str))
                for condition in conditions_str.split(','):
                    for condition_parser in condition_parsers:
                        parsed_condition = condition_parser(condition)
                        if parsed_condition:
                            value_dict.update(parsed_condition)
                parameter_values.append(value_dict)
            else:
                value_dict = __process_parameter_and_tolerance(parameter_str, value_parser)
                parameter_values.append(value_dict)
    return parameter_values


def __decode_parameter_value_common(parameter_str, value_decoder):
    parameter_str = parameter_str.strip()
    if 'max.' in parameter_str:
        parameter_str = parameter_str.replace('max.', '')
        return {'min': None, 'typ': None, 'max': value_decoder(parameter_str)}
    elif 'min.' in parameter_str:
        parameter_str = parameter_str.replace('min.', '')
        return {'min': value_decoder(parameter_str), 'typ': None, 'max': None}
    elif '~' in parameter_str:
        values_str = parameter_str.split('~')
        return {'min': value_decoder(values_str[0]), 'typ': None, 'max': value_decoder(values_str[1])}
    elif '±' in parameter_str:
        #value_str = parameter_str.replace('±', '')
        value_str, tolerance_str = parameter_str.split('±')
        print(parameter_str, "value:", value_str, "tolerance:", tolerance_str)
        if len(value_str) > 0:
            value = value_decoder(value_str)
            if '%' in tolerance_str:
                min_max = percent_str_to_decimal(tolerance_str) / decimal.Decimal(100)
                return {'min': value - value * min_max, 'typ': value, 'max': value + value * min_max}
            else:
                min_max = value_decoder(tolerance_str)
                return {'min': value - min_max, 'typ': value, 'max': value + min_max}
        else:
            min_max = value_decoder(tolerance_str)
            return {'min': min_max * -1, 'typ': None, 'max': min_max}

    else:
        if '+' in parameter_str and '-' in parameter_str:
            value_tolerance = parameter_str.strip().split(' ')
            tolerance = value_tolerance[1].split('/')
            #print(value_tolerance, tolerance)
            value = value_decoder(value_tolerance[0])
            tolerance0 = value_decoder(tolerance[0])
            tolerance1 = value_decoder(tolerance[1])
            print(value, tolerance0, tolerance1)
            if tolerance0 > tolerance1:
                return {'min': value + tolerance1,
                        'typ': value,
                        'max': value + tolerance0}
            else:
                return {'min': value + tolerance0,
                        'typ': value,
                        'max': value + tolerance1}
        elif ' ' in parameter_str:
            typ_and_tolerance = parameter_str.split(' ')
            typ_value = value_decoder(typ_and_tolerance[0])
            tolerance_value = value_decoder(typ_and_tolerance[1])
            if tolerance_value > 0:
                value_dict = {'min': None, 'typ': typ_value, 'max': typ_value + tolerance_value}
            else:
                value_dict = {'min': typ_value + tolerance_value, 'typ': typ_value, 'max': None}
            return value_dict
        elif '+' in parameter_str:
            typ_and_max_str = parameter_str.split('+')
        #         if 'F' in typ_and_max_str[0]:
        #             resistance_typ_str = typ_and_max_str[0]
        #         else:
        #             unit_string = ''.join(item for item in typ_and_max_str[1] if not item.isdigit() and item != '.')
        #             resistance_typ_str = typ_and_max_str[0] + unit_string
        #         print(resistance_str, unit_string)
            typ_value = value_decoder(typ_and_max_str[0])
            max_value = typ_value + value_decoder(typ_and_max_str[1])
            value_dict = {'min': None, 'typ': typ_value, 'max': max_value}
            print(value_dict)
            return value_dict
        else:
            return {'min': None, 'typ': value_decoder(parameter_str), 'max': None}


def decode_integer_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, value_str_to_decimal)
    # if 'max.' in parameter_str:
    #     parameter_str = parameter_str.replace('max.', '')
    #     return {'min': None, 'typ': None, 'max': int(parameter_str)}
    # elif 'min.' in parameter_str:
    #     parameter_str = parameter_str.replace('min.', '')
    #     if parameter_str.strip() == '-':
    #         return
    #     return {'min': int(parameter_str), 'typ': None, 'max': None}
    # elif '~' in parameter_str:
    #     values_str = parameter_str.split('~')
    #     return {'min': int(values_str[0]), 'typ': None, 'max': int(values_str[1])}
    # elif '±' in parameter_str:
    #     value_str = parameter_str.replace('±', '')
    #     return {'min': int(value_str) * -1, 'typ': None, 'max': int(value_str)}
    # else:
    #     return {'min': None, 'typ': int(parameter_str), 'max': None}


def decode_decibel_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, decibel_str_to_decimal)


def decode_melting_integral_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, melting_integral_str_to_decimal)


def decode_ppm_parameter(parameter_str):
    if 'ppm' in parameter_str:
        return decode_integer_parameter(parameter_str.replace('ppm', ''))


def decode_temperature_coefficient_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, tcr_str_to_decimal)


def decode_percent_parameter(parameter_str):
    return decode_integer_parameter(parameter_str.replace('%', ''))


def decode_phase_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, phase_str_to_decimal)


def decode_power_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, power_str_to_decimal)


def decode_resistance_parameter(resistance_str):
    return __decode_parameter_value_common(resistance_str, resistance_str_to_decimal)


def decode_temperature_parameter(parameter_str):
    return __decode_parameter_value_common(parameter_str, celsius_str_to_decimal)


def decode_voltage_parameter(voltage_str):
    return __decode_parameter_value_common(voltage_str, voltage_str_to_decimal)


def decode_current_parameter(current_str):
    return __decode_parameter_value_common(current_str, current_str_to_decimal)


def decode_capacitance_parameter(capacitance_str):
    return __decode_parameter_value_common(capacitance_str, capacitance_str_to_decimal)
    # if 'max.' in capacitance_str:
    #     current_str = capacitance_str.replace('max.', '')
    #     return {'min': None, 'typ': None, 'max': capacitance_str_to_decimal(current_str)}
    # elif 'min.' in capacitance_str:
    #     current_str = capacitance_str.replace('min.', '')
    #     return {'min': capacitance_str_to_decimal(current_str), 'typ': None, 'max': None}
    # else:
    #     if '+' in capacitance_str:
    #         typ_and_max_str = capacitance_str.split('+')
    #         if 'F' in typ_and_max_str[0]:
    #             capacitance_typ_str = typ_and_max_str[0]
    #         else:
    #             unit_string = ''.join(item for item in typ_and_max_str[1] if not item.isdigit() and item != '.')
    #             capacitance_typ_str = typ_and_max_str[0] + unit_string
    #         print(capacitance_str, unit_string)
    #         typ_capacitance = capacitance_str_to_decimal(capacitance_typ_str)
    #         capacitance = {'min': None, 'typ': typ_capacitance,
    #                        'max': typ_capacitance + capacitance_str_to_decimal(typ_and_max_str[1])}
    #         print(capacitance)
    #         return capacitance
    #     else:
    #         return {'min': None, 'typ': capacitance_str_to_decimal(capacitance_str), 'max': None}


def decode_capacity_parameter(capacity_str):
    return __decode_parameter_value_common(capacity_str, capacity_str_to_decimal)


def decode_inductance_parameter(inductance_str):
    return __decode_parameter_value_common(inductance_str, inductance_str_to_decimal)


def decode_distance_parameter(distance_str):
    return __decode_parameter_value_common(distance_str, distance_str_to_decimal)


def decode_dimension_parameter(distance_str):
    return __decode_parameter_value_common(distance_str, distance_str_to_decimal)


def decode_frequency_parameter(frequency_str):
    return __decode_parameter_value_common(frequency_str, frequency_str_to_decimal)


def decode_duration_parameter(frequency_str):
    return __decode_parameter_value_common(frequency_str, duration_str_to_decimal)


def decode_discharge_current_condition(condition_str):
    if 'Id=' in condition_str:
        return {'at_discharge_current': current_str_to_decimal(condition_str.replace('Id=', ''))}


def decode_drain_current_condition(condition_str):
    if 'I_D=' in condition_str:
        return {'at_drain_current': current_str_to_decimal(condition_str.replace('I_D=', ''))}


def decode_gate1_source_voltage_condition(condition_str):
    if 'V_G1S=' in condition_str:
        return {'at_gate1_source_voltage': voltage_str_to_decimal(condition_str.replace('V_G1S=', ''))}


def decode_gate2_source_voltage_condition(condition_str):
    if 'V_G2S=' in condition_str:
        return {'at_gate2_source_voltage': voltage_str_to_decimal(condition_str.replace('V_G2S=', ''))}


def decode_drain_source_voltage_condition(condition_str):
    if 'V_DS=' in condition_str:
        return {'at_drain_source_voltage': voltage_str_to_decimal(condition_str.replace('V_DS=', ''))}


def decode_gate1_source_current_condition(condition_str):
    if 'I_G1S=' in condition_str:
        return {'at_gate1_source_current': current_str_to_decimal(condition_str.replace('I_G1S=', ''))}


def decode_gate2_source_current_condition(condition_str):
    if 'I_G2S=' in condition_str:
        return {'at_gate2_source_current': current_str_to_decimal(condition_str.replace('I_G2S=', ''))}


def decode_gate2_source_voltage_range_condition(condition_str):
    if 'V_G2S=' in condition_str:
        decoded = decode_voltage_parameter(condition_str.replace('V_G2S=', ''))
        return {'at_gate2_source_voltage_range': {'min': decoded['min'], 'max': decoded['max']}}


def decode_current_condition(condition_str):
    if 'A' in condition_str:
        return {'at_current': current_str_to_decimal(condition_str)}


def decode_voltage_condition(condition_str):
    if 'V' in condition_str:
        return {'at_voltage': voltage_str_to_decimal(condition_str)}


def decode_temperature_condition(condition_str):
    if '℃' in condition_str or '°C' in condition_str:
        return {'at_temp': celsius_str_to_decimal(condition_str)}


def decode_ambient_temperature_condition(condition_str):
    if 'TA' in condition_str:
        return {'at_temp': celsius_str_to_decimal(condition_str.replace('TA=', ''))}


def decode_frequency_condition(condition_str):
    if 'f' in condition_str:
        condition_str = condition_str.replace('f=', '')
        return {'at_frequency': frequency_str_to_decimal(condition_str)}
    elif 'Hz' in condition_str:
        return {'at_frequency': frequency_str_to_decimal(condition_str)}


def decode_inductance_drop_condition(condition_str):
    if 'dL' in condition_str:
        inductance_drop = condition_str.replace('dL=', '')
        return {'at_inductance_drop': decode_percent_parameter(inductance_drop)}


def duration_str_to_decimal(duration_str):
    if 's' in duration_str:
        return decimal.Decimal(duration_str.replace('s', ''))


def capacity_str_to_decimal(current_str):
    if 'mAh' in current_str:
        return decimal.Decimal(current_str.replace('mAh', '')) / 1000
    elif 'Ah' in current_str:
        return decimal.Decimal(current_str.replace('Ah', ''))


def current_str_to_decimal(current_str):
    if 'nA' in current_str:
        return decimal.Decimal(current_str.replace('nA', '')) / 1000000000
    elif 'uA' in current_str:
        return decimal.Decimal(current_str.replace('uA', '')) / 1000000
    elif 'mA' in current_str:
        return decimal.Decimal(current_str.replace('mA', '')) / 1000
    elif 'A' in current_str:
        return decimal.Decimal(current_str.replace('A', ''))


def voltage_str_to_decimal(current_str):
    if 'nV' in current_str:
        return decimal.Decimal(current_str.replace('nV', '')) / 1000000000
    elif 'uV' in current_str:
        return decimal.Decimal(current_str.replace('uV', '')) / 1000000
    elif 'mV' in current_str:
        return decimal.Decimal(current_str.replace('mV', '')) / 1000
    elif 'V' in current_str:
        return decimal.Decimal(current_str.replace('V', ''))


def capacitance_str_to_decimal(capacitance_str):
    if 'fF' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('fF', '')) / 1000000000000000
    elif 'pF' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('pF', '')) / 1000000000000
    elif 'nF' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('nF', '')) / 1000000000
    elif 'uF' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('uF', '')) / 1000000
    elif 'mF' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('mF', '')) / 1000
    elif 'F' in capacitance_str:
        return decimal.Decimal(capacitance_str.replace('F', ''))


def resistance_str_to_decimal(resistance_str):
    print('Decoding Resistance:', resistance_str)
    try:
        if 'uR' in resistance_str or 'uΩ' in resistance_str:
            return decimal.Decimal(resistance_str.replace('uR', '').replace('uΩ', '')) / 1000000
        elif 'mR' in resistance_str or 'mΩ' in resistance_str:
            return decimal.Decimal(resistance_str.replace('mR', '').replace('mΩ', '')) / 1000
        elif 'kR' in resistance_str or 'kΩ' in resistance_str:
            return decimal.Decimal(resistance_str.replace('kR', '').replace('kΩ', '')) * 1000
        elif 'MR' in resistance_str or 'MΩ' in resistance_str:
            return decimal.Decimal(resistance_str.replace('MR', '').replace('MΩ', '')) * 1000000
        elif 'GR' in resistance_str or 'MΩ' in resistance_str:
            return decimal.Decimal(resistance_str.replace('GR', '').replace('GΩ', '')) * 1000000000
        elif 'R' in resistance_str or 'Ω' in resistance_str or 'Ω' in resistance_str:
            print("Ohms", resistance_str)
            return decimal.Decimal(resistance_str.replace('R', '').replace('Ω', '').replace('Ω', ''))
        else:
            raise ValueError(resistance_str)
    except:
        raise ValueError(resistance_str)


def frequency_str_to_decimal(frequenc_str):
    if 'mHz' in frequenc_str:
        return decimal.Decimal(frequenc_str.replace('mHz', '')) / 1000
    elif 'kHz' in frequenc_str:
        return decimal.Decimal(frequenc_str.replace('kHz', '')) * 1000
    elif 'MHz' in frequenc_str:
        return decimal.Decimal(frequenc_str.replace('MHz', '')) * 1000000
    elif 'GHz' in frequenc_str:
        return decimal.Decimal(frequenc_str.replace('GHz', '')) * 1000000000
    elif 'Hz' in frequenc_str:
        return decimal.Decimal(frequenc_str.replace('Hz', ''))


def inductance_str_to_decimal(inductance_str):
    if 'pH' in inductance_str:
        return decimal.Decimal(inductance_str.replace('pH', '')) / 1000000000000
    elif 'nH' in inductance_str:
        return decimal.Decimal(inductance_str.replace('nH', '')) / 1000000000
    elif 'uH' in inductance_str or 'μH' in inductance_str:
        return decimal.Decimal(inductance_str.replace('uH', '').replace('μH', '')) / 1000000
    elif 'mH' in inductance_str:
        return decimal.Decimal(inductance_str.replace('mH', '')) / 1000
    elif 'H' in inductance_str:
        return decimal.Decimal(inductance_str.replace('H', ''))


def tcr_str_to_decimal(tcr_str):
    print(tcr_str)
    inductance_str = tcr_str.replace('°C', '℃').replace('°C', '℃')
    if 'ppm/℃' in inductance_str:
        return decimal.Decimal(inductance_str.replace('ppm/℃', ''))
    elif 'ppm/K' in inductance_str:
        return decimal.Decimal(inductance_str.replace('ppm/K', ''))


def percent_str_to_decimal(percent_str):
    if '%' in percent_str:
        return decimal.Decimal(percent_str.replace('%', ''))


def phase_str_to_decimal(phase_str):
    if '°' in phase_str:
        return math.radians(decimal.Decimal(phase_str.replace('°', '')))
    else:
        return decimal.Decimal(phase_str.replace('rad', ''))


def decode_possibly_fractional_value(value_str):
    if "/" in value_str:
        nominator_str, denominator_str = value_str.split("/")
        return decimal.Decimal(nominator_str) / decimal.Decimal(denominator_str)
    else:
        return decimal.Decimal(value_str)


def power_str_to_decimal(power_str):
    if 'pW' in power_str:
        return decimal.Decimal(power_str.replace('pW', '')) / 1000000000000
    elif 'nW' in power_str:
        return decimal.Decimal(power_str.replace('nW', '')) / 1000000000
    elif 'uW' in power_str:
        return decimal.Decimal(power_str.replace('uW', '')) / 1000000
    elif 'mW' in power_str:
        return decimal.Decimal(power_str.replace('mW', '')) / 1000
    elif 'W' in power_str:
        return decode_possibly_fractional_value(power_str.replace('W', ''))


def decibel_str_to_decimal(decibel_str):
    if 'dB' in decibel_str:
        return decimal.Decimal(decibel_str.replace('dB', ''))


def value_str_to_decimal(value_str):
    return decimal.Decimal(value_str)


def distance_str_to_decimal(distance_str):
    if 'mm' in distance_str:
        return decimal.Decimal(distance_str.replace('mm', '')) / 1000
    elif 'cm' in distance_str:
        return decimal.Decimal(distance_str.replace('cm', '')) / 100
    elif 'km' in distance_str:
        return decimal.Decimal(distance_str.replace('km', '')) * 1000
    elif 'm' in distance_str:
        return decimal.Decimal(distance_str.replace('m', ''))


def celsius_str_to_decimal(celsius_str):
    if '°C' in celsius_str or '℃' in celsius_str:
        return decimal.Decimal(celsius_str.replace('°C', '').replace('℃', ''))


def melting_integral_str_to_decimal(melting_integral_str):
    if 'A^2*S' in melting_integral_str:
        return decimal.Decimal(melting_integral_str.replace('A^2*S', ''))


