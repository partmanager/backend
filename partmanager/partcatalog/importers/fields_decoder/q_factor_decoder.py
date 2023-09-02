from partcatalog.models.fields.q_factor import QFactor
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import frequency_decode as __frequency_decode
from .decimal_decoder import decimal_decoder


def q_factor_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], decimal_decoder)
    if value:
        q = QFactor()
        q.min = value['min']
        q.typ = value['typ']
        q.max = value['max']
        if 'conditions' in json_data:
            if 'T' in json_data['conditions']:
                q.at_temp = __si_temperature_decode(json_data['conditions']['T'])
            else:
                q.at_temp = None
            if 'f' in json_data['conditions']:
                q.at_frequency = __frequency_decode(json_data['conditions']['f'])
            else:
                q.at_frequency = None
        else:
            q.at_temp = None
            q.at_frequency = None
        return q
