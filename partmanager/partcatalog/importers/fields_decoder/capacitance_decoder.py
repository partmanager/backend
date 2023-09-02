from decimal import Decimal
from partcatalog.models.fields.capacitance import Capacitance, CapacitanceAtFreq
from partcatalog.models.fields.capacitance import ToleranceType
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import capacitance_decode as __si_capacitance_decode
from .si_unit_decoder import frequency_decode as __frequency_decode


def capacitance_decoder(json_data):
    try:
        value = parameter_str_to_dict(json_data['value'], __si_capacitance_decode)
        if value:
            capacitance = Capacitance()
            capacitance.min = value['min']
            capacitance.typ = value['typ']
            capacitance.max = value['max']
            if 'tolerance_type' in value:
                capacitance.tolerance_type = ToleranceType.from_string(value['tolerance_type'])
                if value['tolerance_type'] == 'relative':
                    capacitance.relative_tolerance = value['relative_tolerance']
                else:
                    value_over = capacitance.max - capacitance.typ
                    value_under = capacitance.min - capacitance.typ
                    tolerance = max(abs(value_over), abs(value_under))
                    capacitance.relative_tolerance = (tolerance / capacitance.typ) * Decimal(100)
            else:
                capacitance.tolerance_type = ToleranceType.RELATIVE
                capacitance.relative_tolerance = None
            return capacitance
    except IndexError as error:
        print(error)
        print(json_data)
        exit(-1)


def capacitance_at_frequency_decoder(json_data):
    assert len(json_data['conditions']) == 1
    value = parameter_str_to_dict(json_data['value'], __si_capacitance_decode)
    if value:
        capacitance = CapacitanceAtFreq()
        capacitance.min = value['min']
        capacitance.typ = value['typ']
        capacitance.max = value['max']
        capacitance.at_frequency = __frequency_decode(json_data['conditions']['f'])
        return capacitance


