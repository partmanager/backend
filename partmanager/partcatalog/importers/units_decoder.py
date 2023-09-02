from .parameter_decoder import decode_parameter_and_tolerance, decode_capacitance_parameter, decode_capacity_parameter, \
    decode_decibel_parameter, decode_dimension_parameter, decode_frequency_parameter, decode_phase_parameter, \
    decode_power_parameter, \
    decode_resistance_parameter, decode_current_parameter, decode_voltage_parameter, celsius_str_to_decimal, \
    decode_parameter, decode_percent_parameter, decode_integer_parameter, decode_temperature_coefficient_parameter
from .parameter_decoder import decode_current_condition, decode_ambient_temperature_condition, \
    decode_discharge_current_condition, \
    decode_frequency_condition, decode_inductance_drop_condition, decode_melting_integral_parameter, \
    decode_drain_current_condition, decode_gate1_source_voltage_condition, decode_gate2_source_voltage_condition, \
    decode_drain_source_voltage_condition, decode_gate1_source_current_condition, decode_gate2_source_current_condition,\
    decode_gate2_source_voltage_range_condition


def decode_battery_capacity(battery_capacity_str, field_name, max_field_count=1):
    if battery_capacity_str:
        impedances = decode_parameter(battery_capacity_str, decode_capacity_parameter,
                                      [decode_ambient_temperature_condition, decode_discharge_current_condition])
        print("Decoded", impedances)
        response = {}
        for index, impedance in enumerate(impedances):
            response.update({field_name + '_{}_min'.format(index + 1): impedance['min'],
                             field_name + '_{}_typ'.format(index + 1): impedance['typ'],
                             field_name + '_{}_max'.format(index + 1): impedance['max'],
                             '{}_{}_at_discharge_current'.format(field_name, index + 1): impedance[
                                 'at_discharge_current'],
                             '{}_{}_at_temp'.format(field_name, index + 1): impedance['at_temp']})
        return response
    else:
        return {}


def decode_capacitance_cond_freq(capacitance_str, field_name):
    if capacitance_str:
        impedance = decode_parameter(capacitance_str, decode_capacitance_parameter, [decode_frequency_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                field_name + '_at_frequency': impedance[0]['at_frequency']}
    else:
        return {}


def decode_decibel(decibel_str, field_name):
    if decibel_str:
        impedance = decode_parameter(decibel_str, decode_decibel_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_dimension(dimension_str, field_name):
    if dimension_str:
        impedance = decode_parameter(dimension_str, decode_dimension_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_drain_source_breakdown_voltage(vds_str, field_name):
    if vds_str:
        impedance = decode_parameter(vds_str, decode_voltage_parameter, [decode_drain_current_condition,
                                                                         decode_gate1_source_voltage_condition,
                                                                         decode_gate2_source_voltage_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_current'.format(field_name): impedance[0]['at_drain_current']}
    else:
        return {}


def decode_gate1_source_breakdown_voltage(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_voltage_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate1_source_current_condition,
                                                                         decode_gate2_source_voltage_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate1_source_current'.format(field_name): impedance[0]['at_gate1_source_current'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage']}
    else:
        return {}


def decode_gate2_source_breakdown_voltage(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_voltage_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate2_source_current_condition,
                                                                         decode_gate1_source_voltage_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate2_source_current'.format(field_name): impedance[0]['at_gate2_source_current'],
                '{}_at_gate1_source_voltage'.format(field_name): impedance[0]['at_gate1_source_voltage']}
    else:
        return {}


def decode_gate1_source_leakage_current(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_voltage_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate1_source_voltage_condition,
                                                                         decode_gate2_source_voltage_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate1_source_voltage'.format(field_name): impedance[0]['at_gate1_source_voltage'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage']}
    else:
        return {}


def decode_gate2_source_leakage_current(vgs_str, field_name):
    return decode_gate1_source_leakage_current(vgs_str, field_name)


def decode_drain_current(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_current_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate1_source_voltage_condition,
                                                                         decode_gate2_source_voltage_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate1_source_voltage'.format(field_name): impedance[0]['at_gate1_source_voltage'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage']}
    else:
        return {}


def decode_gate1_source_pinch_off_voltage(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_voltage_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate2_source_voltage_condition,
                                                                         decode_drain_current_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage'],
                '{}_at_drain_current'.format(field_name): impedance[0]['at_drain_current']}
    else:
        return {}


def decode_gate2_source_pinch_off_voltage(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_voltage_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate1_source_voltage_condition,
                                                                         decode_drain_current_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate1_source_voltage'.format(field_name): impedance[0]['at_gate1_source_voltage'],
                '{}_at_drain_current'.format(field_name): impedance[0]['at_drain_current']}
    else:
        return {}


def decode_forward_transconductance(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_integer_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate2_source_voltage_condition,
                                                                         decode_drain_current_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage'],
                '{}_at_drain_current'.format(field_name): impedance[0]['at_drain_current']}
    else:
        return {}


def decode_gate1_input_capacitance(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_capacitance_parameter, [decode_drain_source_voltage_condition,
                                                                             decode_gate2_source_voltage_condition,
                                                                             decode_drain_current_condition,
                                                                             decode_frequency_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate2_source_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage'],
                '{}_at_drain_current'.format(field_name): impedance[0]['at_drain_current'],
                '{}_at_frequency'.format(field_name): impedance[0]['at_frequency']}
    else:
        return {}


def decode_gate2_input_capacitance(vgs_str, field_name):
    return decode_gate1_input_capacitance(vgs_str, field_name)


def decode_feedback_capacitance(vgs_str, field_name):
    return decode_gate1_input_capacitance(vgs_str, field_name)


def decode_output_capacitance(vgs_str, field_name):
    return decode_gate1_input_capacitance(vgs_str, field_name)


def decode_power_gain(vgs_str, field_name, field_count):
    if vgs_str:
        power_gain_list = decode_parameter(vgs_str, decode_decibel_parameter, [decode_drain_source_voltage_condition,
                                                                               decode_gate2_source_voltage_condition,
                                                                               decode_drain_current_condition,
                                                                               decode_frequency_condition])
        response = {}
        for index, power_gain in enumerate(power_gain_list):
            response.update({'{}_{}_min'.format(field_name, index + 1): power_gain['min'],
                             '{}_{}_typ'.format(field_name, index + 1): power_gain['typ'],
                             '{}_{}_max'.format(field_name, index + 1): power_gain['max'],
                             '{}_{}_at_drain_source_voltage'.format(field_name, index + 1): power_gain['at_drain_source_voltage'],
                             '{}_{}_at_gate2_source_voltage'.format(field_name, index + 1): power_gain['at_gate2_source_voltage'],
                             '{}_{}_at_drain_current'.format(field_name, index + 1): power_gain['at_drain_current'],
                             '{}_{}_at_frequency'.format(field_name, index + 1): power_gain['at_frequency']})
        return response
    else:
        return {}


def decode_noise_figure(vgs_str, field_name, field_count):
    return decode_power_gain(vgs_str, field_name, field_count)


def decode_gain_control_range(vgs_str, field_name):
    if vgs_str:
        impedance = decode_parameter(vgs_str, decode_decibel_parameter, [decode_drain_source_voltage_condition,
                                                                         decode_gate2_source_voltage_range_condition,
                                                                         decode_frequency_condition])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max'],
                '{}_at_drain_source_voltage'.format(field_name): impedance[0]['at_drain_source_voltage'],
                '{}_at_gate2_source_min_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage_range'][
                    'min'],
                '{}_at_gate2_source_max_voltage'.format(field_name): impedance[0]['at_gate2_source_voltage_range'][
                    'max'],
                '{}_at_frequency'.format(field_name): impedance[0]['at_frequency']}
    else:
        return {}


def decode_frequency_range(frequency_range_str, field_name):
    if frequency_range_str:
        frequency = decode_parameter(frequency_range_str, decode_frequency_parameter, [])
        return {field_name + '_min': frequency[0]['min'],
                field_name + '_max': frequency[0]['max']}
    else:
        return {}


def decode_impedance(impedance_str, field_name):
    if impedance_str:
        impedance = decode_parameter(impedance_str, decode_resistance_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_melting_integral(melting_integral_str, field_name):
    if melting_integral_str:
        impedance = decode_parameter(melting_integral_str, decode_melting_integral_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_phase(phase_str, field_name):
    if phase_str:
        impedance = decode_parameter(phase_str, decode_phase_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_power(power_str, field_name):
    if power_str:
        impedance = decode_parameter(power_str, decode_power_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}


def decode_return_loss(return_loss_str, field_name):
    if return_loss_str:
        return_loss = decode_parameter(return_loss_str, decode_decibel_parameter, [])
        return {field_name + '_min': return_loss[0]['min'],
                field_name + '_typ': return_loss[0]['typ'],
                field_name + '_max': return_loss[0]['max']}
    else:
        return {}


def decode_dc_resistance(dc_resistance_str, field_name):
    if dc_resistance_str:
        #resistance = decode_resistance_parameter(dc_resistance_str)
        resistance = decode_parameter_and_tolerance(dc_resistance_str, decode_resistance_parameter, [])
        print(resistance)
        value = resistance[0]['value']
        tolerance = resistance[0]['tolerance']
        if value:
            min = value - value * resistance[0]['tolerance']['over'] if resistance[0]['tolerance'][
                                                                            'type'] == '%' else value + resistance[0][
                'tolerance']['over']
            max = value + value * resistance[0]['tolerance']['over'] if resistance[0]['tolerance'][
                                                                            'type'] == '%' else value + resistance[0][
                'tolerance']['over']
            return {field_name + '_min': min,
                    field_name + '_typ': value,
                    field_name + '_max': max,
                    field_name + '_at_temp': 25}
        else:
            return {field_name + '_typ': None,
                    field_name + '_max': tolerance['over'],
                    field_name + '_at_temp': 25}
    else:
        return {}


def decode_resistance(resistance_str, field_name):
    if resistance_str:
        resistance = decode_parameter(resistance_str, decode_resistance_parameter, [])
        return {field_name + '_min': resistance[0]['min'],
                field_name + '_typ': resistance[0]['typ'],
                field_name + '_max': resistance[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


def decode_insulation_resistance(insulation_resistance_str, field_name):
    if insulation_resistance_str:
        resistance = decode_parameter(insulation_resistance_str, decode_resistance_parameter, [])
        return {field_name + '_typ': resistance[0]['typ'],
                field_name + '_max': resistance[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


# def decode_dc_current(dictionary, dictionary_field_name, field_name):
#     for key in dictionary:
#         if dictionary_field_name in key:
#             dc_rated_current_str = dictionary[key]
#             at_temperature = celsius_str_to_decimal(key.replace('DC Rated Current @', '')) if '@' in key else None
#             if dc_rated_current_str:
#                 dc_rated_current = decode_current_parameter(dc_rated_current_str)
#                 dc_rated_current['at_temp'] = at_temperature
#                 return {field_name + '_' + k: v for k, v in dc_rated_current.items()}
#     return {}

def decode_dc_current(dc_current_str, field_name):
    if dc_current_str:
        voltage = decode_parameter(dc_current_str, decode_current_parameter, [])
        return {field_name + '_min': voltage[0]['min'],
                field_name + '_typ': voltage[0]['typ'],
                field_name + '_max': voltage[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


def decode_dc_saturation_current(dc_current_str, field_name):
    if dc_current_str:
        voltage = decode_parameter(dc_current_str, decode_current_parameter,
                                   [decode_inductance_drop_condition, decode_ambient_temperature_condition])
        return {field_name + '_min': voltage[0]['min'],
                field_name + '_typ': voltage[0]['typ'],
                field_name + '_max': voltage[0]['max'],
                field_name + '_at_temp': voltage[0]['at_temp'],
                field_name + '_at_inductance_drop': voltage[0]['at_inductance_drop']['typ']}
    else:
        return {}


def decode_dc_voltage(dc_voltage_str, field_name):
    if dc_voltage_str:
        voltage = decode_parameter(dc_voltage_str, decode_voltage_parameter, [])
        return {field_name + '_min': voltage[0]['min'],
                field_name + '_typ': voltage[0]['typ'],
                field_name + '_max': voltage[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


def decode_max_current(max_current_str, field_name):
    if max_current_str:
        current = decode_parameter(max_current_str, decode_current_parameter, [])
        return {field_name + '_max': current[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


def decode_max_voltage(max_voltage_str, field_name):
    if max_voltage_str:
        voltage = decode_parameter(max_voltage_str, decode_voltage_parameter, [])
        return {field_name + '_max': voltage[0]['max'],
                field_name + '_at_temp': 25}
    else:
        return {}


def decode_time_at_current(max_time_current_str, field_name):
    if max_time_current_str:
        voltage = decode_parameter(max_time_current_str, decode_voltage_parameter, [decode_current_condition])
        return {field_name + '_max': voltage[0]['max'],
                field_name + '_at_temp': 25,
                field_name + '_at_current': voltage[0]['at_current']}
    else:
        return {}


def decode_temperature_coefficient(tcr_str, field_name):
    if tcr_str:
        impedance = decode_parameter(tcr_str, decode_temperature_coefficient_parameter, [])
        return {field_name + '_min': impedance[0]['min'],
                field_name + '_typ': impedance[0]['typ'],
                field_name + '_max': impedance[0]['max']}
    else:
        return {}
