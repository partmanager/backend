from partcatalog.models.fields.temperature_coefficient import TemperatureCoefficient
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import ppm_per_deg_decode as __ppm_per_deg_decode


def temperature_coefficient_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __ppm_per_deg_decode)
    if value:
        tc = TemperatureCoefficient()
        tc.min = value['min']
        tc.typ = value['typ']
        tc.max = value['max']
        return tc
