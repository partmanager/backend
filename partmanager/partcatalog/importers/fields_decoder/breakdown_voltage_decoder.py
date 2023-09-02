from partcatalog.models.fields.breakdown_voltage import BreakdownVoltage
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import voltage_decode as __voltage_decode
from .si_unit_decoder import current_decode as __current_decode


def breakdown_voltage_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        breakdown_voltage = BreakdownVoltage()
        breakdown_voltage.min = value['min']
        breakdown_voltage.typ = value['typ']
        breakdown_voltage.max = value['max']
        if 'conditions' in json_data:
            breakdown_voltage.at_reverse_current_uA = __current_decode(json_data['conditions']['I_R']) * 1000000
        else:
            breakdown_voltage.at_reverse_current_uA = None
        return breakdown_voltage
