from partcatalog.models.fields.forward_voltage import ForwardVoltage
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import current_decode as __si_current_decode
from .si_unit_decoder import voltage_decode as __voltage_decode


def forward_voltage_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        forward_voltage = ForwardVoltage()
        forward_voltage.min = value['min']
        forward_voltage.typ = value['typ']
        forward_voltage.max = value['max']
        if 'conditions' in json_data:
            parsed_conditions = 0
            if 'T_j' in json_data['conditions']:
                parsed_conditions += 1
                forward_voltage.at_junction_temp = __si_temperature_decode(json_data['conditions']['T_j'])
            elif 'Tj' in json_data['conditions']:
                parsed_conditions += 1
                forward_voltage.at_junction_temp = __si_temperature_decode(json_data['conditions']['Tj'])
            elif 'T_A' in json_data['conditions']:
                parsed_conditions += 1
                forward_voltage.at_junction_temp = __si_temperature_decode(json_data['conditions']['T_A'])
            else:
                forward_voltage.at_junction_temp = None

            if 'I_F' in json_data['conditions']:
                parsed_conditions += 1
                forward_voltage.at_forward_current = __si_current_decode(json_data['conditions']['I_F'])
            elif 'IF' in json_data['conditions']:
                parsed_conditions += 1
                forward_voltage.at_forward_current = __si_current_decode(json_data['conditions']['IF'])
            else:
                forward_voltage.at_forward_current = None

            if len(json_data['conditions']) != parsed_conditions:
                print("Unexpected condition in forward_voltage_decoder: ", json_data)
        else:
            forward_voltage.at_junction_temp = None
            forward_voltage.at_forward_current = None
        return forward_voltage
