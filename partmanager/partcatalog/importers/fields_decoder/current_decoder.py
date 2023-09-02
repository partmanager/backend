from partcatalog.models.fields.current import CurrentAtTemp
from partcatalog.models.fields.current import Current
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __si_current_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def current_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        current = Current()
        current.min = value['min']
        current.typ = value['typ']
        current.max = value['max']
        return current


def current_at_temp_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        current = CurrentAtTemp()
        current.min = value['min']
        current.typ = value['typ']
        current.max = value['max']
        if 'conditions' in json_data:
            parsed_conditions = 0
            if 'T_A' in json_data['conditions']:
                parsed_conditions += 1
                current.at_temp = __si_temperature_decode(json_data['conditions']['T_A'])
            elif 'TA' in json_data['conditions']:
                parsed_conditions += 1
                current.at_temp = __si_temperature_decode(json_data['conditions']['TA'])
                print('Deprecated condition string: "TA" for ambient temperature please use: "T_A"')
            elif 'T_C' in json_data['conditions']:
                parsed_conditions += 1
                current.at_temp = __si_temperature_decode(json_data['conditions']['T_C'])
            else:
                current.at_temp = None

            if len(json_data['conditions']) != parsed_conditions:
                print("Unexpected condition in current_at_temp_decoder: ", json_data)
        else:
            current.at_temp = None
        return current

