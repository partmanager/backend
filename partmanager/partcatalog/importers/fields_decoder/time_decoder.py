from .si_unit_decoder import time_decode as __si_time_decode
from .si_unit_decoder import voltage_decode as __si_voltage_decode
from .si_unit_decoder import current_decode as __si_current_decode
from .field_decoder_common import parameter_str_to_dict
from partcatalog.models.fields.time import Time
from partcatalog.models.fields.fall_time import FallTime
from partcatalog.models.fields.rise_time import RiseTime
from partcatalog.models.fields.supply_voltage_range import SupplyVoltageRange


def bool_decoder(json_data):
    return json_data['value'] == 'yes'


def frequency_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_frequency_decode)
    if value:
        return RiseTime(min=value['min'], typ=value['typ'], max=value['max'])


def frequency_stability_decoder(json_data):
    pass


def time_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_time_decode)
    if value:
        time = Time()
        time.min = value['min']
        time.typ = value['typ']
        time.max = value['max']
        return time


def fall_time_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_time_decode)
    if value:
        fall_time = FallTime()
        fall_time.min = value['min']
        fall_time.typ = value['typ']
        fall_time.max = value['max']
        return fall_time


def rise_time_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_time_decode)
    if value:
        rise_time = RiseTime()
        rise_time.min = value['min']
        rise_time.typ = value['typ']
        rise_time.max = value['max']
        return rise_time


def supply_current_range_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        voltage_range = SupplyVoltageRange()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        return voltage_range


def supply_voltage_range_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_voltage_decode)
    if value:
        voltage_range = SupplyVoltageRange()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        return voltage_range



