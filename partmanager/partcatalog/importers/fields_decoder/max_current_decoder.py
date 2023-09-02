from partcatalog.models.fields.max_current import MaxCurrentAtTemp, MaxCurrentAtTempAtFreq
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import frequency_decode as __frequency_decode


def max_current_at_temp_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __current_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        power = MaxCurrentAtTemp()
        power.max = value['max']
        if 'conditions' in json_data:
            power.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        else:
            power.at_temp = None
        return power


def max_current_at_temp_at_freq_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __current_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        current = MaxCurrentAtTempAtFreq()
        current.max = value['max']
        if 'conditions' in json_data:
            current.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
            current.at_freq = __frequency_decode(json_data['conditions']['f']) if 'f' in json_data['conditions'] else None
        else:
            current.at_temp = None
            current.at_freq = None
        return current
