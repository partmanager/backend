from partcatalog.models.fields.ageing import Ageing
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import ppm_per_year_decode as ppm_per_year_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def ageing_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], ppm_per_year_decode)
    if value:
        voltage_range = Ageing()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        if 'conditions' in json_data:
            voltage_range.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        else:
            voltage_range.at_temp = None
        return voltage_range
