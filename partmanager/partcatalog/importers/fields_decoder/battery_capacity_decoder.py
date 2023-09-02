from partcatalog.models.fields.battery_capacity import BatteryCapacity
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import capacity_decode as __capacity_decode
from .si_unit_decoder import current_decode as __current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def battery_capacity_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __capacity_decode)
    if value:
        battery_capacity = BatteryCapacity()
        battery_capacity.min = value['min']
        battery_capacity.typ = value['typ']
        battery_capacity.max = value['max']
        battery_capacity.at_discharge_current = __current_decode(json_data['conditions']['Id'])
        battery_capacity.at_temp = __si_temperature_decode(json_data['conditions']['TA']) if 'TA' in json_data['conditions'] else None
        return battery_capacity
