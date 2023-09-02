from partcatalog.models.fields.thermal_resistance import ThermalResistance
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import thermal_resistance as __thermal_resistance_decode


def thermal_resistance_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __thermal_resistance_decode)
    if value:
        tr = ThermalResistance()
        tr.min = value['min']
        tr.typ = value['typ']
        tr.max = value['max']
        return tr
