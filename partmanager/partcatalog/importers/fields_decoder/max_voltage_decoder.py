from partcatalog.models.fields.max_voltage import MaxVoltage, MaxVoltageAtTemp
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import voltage_decode as __voltage_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def max_voltage_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        voltage = MaxVoltage()
        voltage.max = value['max']
        return voltage


def max_voltage_at_temp_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        assert value['min'] is None and value['typ'] is None, value
        voltage = MaxVoltageAtTemp()
        voltage.max = value['max']
        if 'conditions' in json_data:
            voltage.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        else:
            voltage.at_temp = None
        return voltage
