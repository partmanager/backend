from partcatalog.models.fields.insulation_resistance import InsulationResistance
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import resistance_decode as __resistance_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import voltage_decode as __voltage_decode


def insulation_resistance_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __resistance_decode)
    if value:
        resistance = InsulationResistance()
        resistance.min = value['min']
        resistance.typ = value['typ']
        resistance.max = value['max']
        if 'conditions' in json_data:
            resistance.at_voltage = __voltage_decode(json_data['conditions']['V']) if 'V' in json_data['conditions'] else None
            resistance.at_temp = __si_temperature_decode(json_data['conditions']['T_A']) if 'T_A' in json_data['conditions'] else None
        else:
            resistance.at_voltage = None
            resistance.at_temp = None
        return resistance
