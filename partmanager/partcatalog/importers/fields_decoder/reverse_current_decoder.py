from partcatalog.models.fields.reverse_current import ReverseCurrent
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __si_temperature_decode
from .si_unit_decoder import current_decode as __si_current_decode
from .si_unit_decoder import voltage_decode as __voltage_decode


def reverse_current_decoder(json_data):
    if isinstance(json_data, list):
        json_data = json_data[0]
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        rc = ReverseCurrent()
        rc.min = value['min']
        rc.typ = value['typ']
        rc.max = value['max']
        if 'conditions' in json_data:
            conditions = json_data['conditions']
            if 'T_j' in conditions:
                rc.at_junction_temp = __si_temperature_decode(conditions['T_j'])
            elif 'Tj' in conditions:
                rc.at_junction_temp = __si_temperature_decode(conditions['Tj'])
            else:
                rc.at_junction_temp = None
            rc.at_ambient_temp = __si_temperature_decode(conditions['T_A']) if 'T_A' in json_data['conditions'] else None
            if 'V_R' in conditions:
                rc.at_reverse_voltage = __voltage_decode(conditions['V_R'])  # V_R
            elif 'VR' in conditions:
                rc.at_reverse_voltage = __voltage_decode(conditions['VR'])  # V_R
        return rc
