from decimal import Decimal
from partcatalog.models.fields.resistance import Resistance, ResistanceAtTemp
from partcatalog.models.fields.resistance import ToleranceType
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import resistance_decode as __resistance_decode
from .si_unit_decoder import temperature_decode as __si_temperature_decode


def resistance_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __resistance_decode)
    if value:
        resistance = Resistance()
        resistance.min = value['min']
        resistance.typ = value['typ']
        resistance.max = value['max']
        if 'tolerance_type' in value:
            resistance.tolerance_type = ToleranceType.from_string(value['tolerance_type'])
            if value['tolerance_type'] == 'relative':
                resistance.relative_tolerance = value['relative_tolerance']
            else:
                value_over = resistance.max - resistance.typ
                value_under = resistance.min - resistance.typ
                tolerance = max(abs(value_over), abs(value_under))
                resistance.relative_tolerance = (tolerance / resistance.typ) * Decimal(100)
        else:
            resistance.tolerance_type = ToleranceType.RELATIVE
            resistance.relative_tolerance = None
        return resistance


def resistance_at_temp_decoder(json_data):
    value = resistance_decoder(json_data)
    if value:
        resistance = ResistanceAtTemp()
        resistance.min = value.min
        resistance.typ = value.typ
        resistance.max = value.max
        resistance.tolerance_type = value.tolerance_type
        resistance.relative_tolerance = value.relative_tolerance
        if 'conditions' in json_data:
            parsed_conditions = 0
            if 'T_A' in json_data['conditions']:
                parsed_conditions += 1
                resistance.at_temp = __si_temperature_decode(json_data['conditions']['T_A'])
            elif 'TA' in json_data['conditions']:
                parsed_conditions += 1
                resistance.at_temp = __si_temperature_decode(json_data['conditions']['TA'])

            if len(json_data['conditions']) != parsed_conditions:
                print("Unexpected condition in resistance_at_temp_decoder: ", json_data)
        else:
            resistance.at_temp = None
        return resistance
