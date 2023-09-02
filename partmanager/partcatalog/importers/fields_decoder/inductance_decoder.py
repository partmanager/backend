from partcatalog.models.fields.inductance import InductanceAtFrequencyAtTemp
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import inductance_decode as __si_inductance_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import frequency_decode as __si_frequency_decoder


def inductance_at_frequency_at_temp_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_inductance_decode)
    if value:
        inductance = InductanceAtFrequencyAtTemp()
        inductance.min = value['min']
        inductance.typ = value['typ']
        inductance.max = value['max']
        if 'conditions' in json_data:
            inductance.at_frequency = __si_frequency_decoder(json_data['conditions']['f']) if 'f' in json_data['conditions'] else None
            inductance.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        else:
            inductance.at_frequency = None
            inductance.at_temp = None
        return inductance
