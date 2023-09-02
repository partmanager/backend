import decimal
from partcatalog.models.fields.melting_integral import MeltingIntegral
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def __melting_integral_from_str(melting_integral_str):
    return decimal.Decimal(melting_integral_str.replace('A^2*S', ''))


def melting_integral_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __melting_integral_from_str)
    if value:
        mi = MeltingIntegral()
        mi.min = value['min']
        mi.typ = value['typ']
        mi.max = value['max']
        if 'conditions' in json_data:
            mi.at_temp = __si_temperature_decode(json_data['conditions']['TA']) if 'TA' in json_data['conditions'] else None
        else:
            mi.at_temp = None
        return mi
