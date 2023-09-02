from partcatalog.models.fields.supply_current_range import SupplyCurrentRange
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import current_decode as __si_current_decode


def supply_current_range_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __si_current_decode)
    if value:
        voltage_range = SupplyCurrentRange()
        voltage_range.min = value['min']
        voltage_range.typ = value['typ']
        voltage_range.max = value['max']
        return voltage_range

