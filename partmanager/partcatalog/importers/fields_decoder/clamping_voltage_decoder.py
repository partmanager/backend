from partcatalog.models.fields.clamping_voltage import ClampingVoltage
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import voltage_decode as __voltage_decode
from .si_unit_decoder import current_decode as __current_decode


def clamping_voltage_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __voltage_decode)
    if value:
        voltage = ClampingVoltage()
        #value['min']
        #value['typ']
        voltage.max = value['max']
        if 'conditions' in json_data:
            if "I" in json_data['conditions']:
                voltage.at_peak_current = __current_decode(json_data['conditions']['I'])
            elif "I_PP" in json_data['conditions']:
                voltage.at_peak_current = __current_decode(json_data['conditions']['I_PP'])
        else:
            voltage.at_peak_current = None
        return voltage
