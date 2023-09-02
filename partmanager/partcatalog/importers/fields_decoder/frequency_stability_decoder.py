from partcatalog.models.fields.frequency_stability import FrequencyStability
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import ppm_decode as __ppm_decode


def frequency_stability_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __ppm_decode)
    if value:
        voltage_range = FrequencyStability()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        return voltage_range
