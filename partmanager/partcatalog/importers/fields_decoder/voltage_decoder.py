from partcatalog.models.fields.voltage import Voltage
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import voltage_decode as __voltage_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def voltage_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        voltage = Voltage()
        voltage.min = value['min']
        voltage.typ = value['typ']
        voltage.max = value['max']
        if 'conditions' in json_data:
            voltage.at_temp = __si_temperature_decode(json_data['conditions']['T_A'])
        else:
            voltage.at_temp = None
        return voltage
