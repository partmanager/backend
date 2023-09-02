from decimal import Decimal
from partcatalog.models.fields.impedance import ImpedanceAtFreq
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import resistance_decode as __resistance_decode
from .si_unit_decoder import frequency_decode as __frequency_decode


def impedance_at_freq_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __resistance_decode)
    if value:
        impedance = ImpedanceAtFreq()
        impedance.min = value['min']
        impedance.typ = value['typ']
        impedance.max = value['max']
        if 'conditions' in json_data:
            impedance.at_frequency = __frequency_decode(json_data['conditions']['f'])
        else:
            impedance.at_frequency = None
        if 'tolerance_type' in value:
            if value['tolerance_type'] == 'relative':
                impedance.tolerance = value['relative_tolerance']
            else:
                value_over = impedance.max - impedance.typ
                value_under = impedance.min - impedance.typ
                tolerance = max(abs(value_over), abs(value_under))
                impedance.tolerance = (tolerance / impedance.typ) * Decimal(100)
        else:
            impedance.tolerance = None
        return impedance
