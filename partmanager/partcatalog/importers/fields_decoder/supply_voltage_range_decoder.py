from partcatalog.models.fields.supply_voltage_range import SupplyVoltageRange
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import voltage_decode as __si_voltage_decode


def supply_voltage_range_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_voltage_decode)
    if value:
        voltage_range = SupplyVoltageRange()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        return voltage_range

