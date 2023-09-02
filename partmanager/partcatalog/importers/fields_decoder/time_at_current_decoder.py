from partcatalog.models.fields.time_at_current import TimeAtCurrent
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import time_decode as __time_decode


def time_at_current_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __time_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        time_at_current = TimeAtCurrent()
        time_at_current.max = value['max']
        time_at_current.at_current = __current_decode(json_data['conditions']['I']) if 'I' in json_data['conditions'] else None
        time_at_current.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        return time_at_current
