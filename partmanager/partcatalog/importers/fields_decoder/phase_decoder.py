from partcatalog.models.fields.phase import phase_from_degree
from .field_decoder_common import parameter_str_to_dict
from ..parameter_decoder import phase_str_to_decimal


def phase_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], phase_str_to_decimal)
    if value:
        return value
