from partcatalog.models.fields.dc_saturation_current import DCSaturationCurrent
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __si_current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def dc_saturation_current_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        current = DCSaturationCurrent()
        current.min = value['min']
        current.typ = value['typ']
        current.max = value['max']
        if 'conditions' in json_data:
            if 'T' in json_data['conditions']:
                current.at_temp = __si_temperature_decode(json_data['conditions']['T'])
            else:
                current.at_temp = None
            if 'dI' in json_data['conditions']:
                current.at_inductance_drop = __si_temperature_decode(json_data['conditions']['dI'])
            else:
                current.at_inductance_drop = None
        else:
            current.at_temp = None
            current.at_inductance_drop = None
        return current

