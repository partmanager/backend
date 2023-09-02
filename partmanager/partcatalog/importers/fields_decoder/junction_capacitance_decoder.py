from decimal import Decimal
from partcatalog.models.fields.junction_capacitance import JunctionCapacitance
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import capacitance_decode as __si_capacitance_decode
from .si_unit_decoder import frequency_decode as __frequency_decode
from .si_unit_decoder import voltage_decode as __voltage_decode


def junction_capacitance_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_capacitance_decode)
    if value:
        capacitance = JunctionCapacitance()
        capacitance.min = value['min']
        capacitance.typ = value['typ'] * Decimal('1e12') if value['typ'] else None
        capacitance.max = value['max'] * Decimal('1e12') if value['max'] else None
        if 'conditions' in json_data:
            conditions = json_data['conditions']
            capacitance.at_frequency = __frequency_decode(json_data['conditions']['f'])
            if 'V_R' in conditions:
                capacitance.at_reverse_voltage = __voltage_decode(json_data['conditions']['V_R'])
            elif 'VR' in conditions:
                capacitance.at_reverse_voltage = __voltage_decode(json_data['conditions']['VR'])
        #print(capacitance.typ)
        return capacitance
