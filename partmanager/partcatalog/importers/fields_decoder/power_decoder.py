from partcatalog.models.fields.power import Power
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import power_decode as __power_decode


def power_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __power_decode)
    if value:
        power = Power()
        power.min = value['min']
        power.typ = value['typ']
        power.max = value['max']
        return power