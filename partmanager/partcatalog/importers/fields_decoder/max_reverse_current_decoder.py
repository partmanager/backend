from partcatalog.models.fields.reverse_current import MaxReverseCurrent
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import voltage_decode as __voltage_decode


def max_reverse_current_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __current_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        current = MaxReverseCurrent()
        current.max = value['max']
        if 'conditions' in json_data:
            current.at_junction_temp = __si_temperature_decode(json_data['conditions']['T_J']) if 'T_J' in json_data['conditions'] else None
            current.at_reverse_voltage = __voltage_decode(json_data['conditions']['V_R']) if 'V_R' in json_data['conditions'] else None
        else:
            current.at_junction_temp = None
            current.at_reverse_voltage = None
        return current
