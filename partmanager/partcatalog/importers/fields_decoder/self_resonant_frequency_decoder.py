from partcatalog.models.fields.self_resonant_frequency import SelfResonantFrequency
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import frequency_decode as __frequency_decode


def self_resonant_frequency_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __frequency_decode)
    if value:
        sfr = SelfResonantFrequency()
        sfr.min = value['min']
        sfr.typ = value['typ']
        sfr.max = value['max']
        if 'conditions' in json_data:
            sfr.at_temp = __si_temperature_decode(json_data['conditions']['T']) if 'T' in json_data['conditions'] else None
        else:
            sfr.at_temp = None
        return sfr
