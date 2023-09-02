from partcatalog.models.fields.decibel import Decibel
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import dB_decode as __dB_decode


def decibel_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __dB_decode)
    if value:
        decibel = Decibel()
        decibel.min = value['min']
        decibel.typ = value['typ']
        decibel.max = value['max']
        return decibel
