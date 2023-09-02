from partcatalog.models.fields.max_power import MaxPower
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import power_decode as __power_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def max_power_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __power_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        power = MaxPower()
        power.max = value['max']
        if 'conditions' in json_data:
            if 'T_A' in json_data['conditions']:
                power.at_temp = __si_temperature_decode(json_data['conditions']['T_A'])
            elif 'TA' in json_data['conditions']:
                power.at_temp = __si_temperature_decode(json_data['conditions']['TA'])
            else:
                power.at_temp = None
        else:
            power.at_temp = None
        return power
