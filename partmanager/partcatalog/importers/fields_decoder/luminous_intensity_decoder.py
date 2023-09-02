from partcatalog.models.fields.luminous_intensity import LuminousIntensity
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import luminous_intensity_decode as __luminous_intensity_decode


def luminous_intensity_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __luminous_intensity_decode)
    if value:
        luminous_intensity = LuminousIntensity()
        luminous_intensity.min = value['min']
        luminous_intensity.typ = value['typ']
        luminous_intensity.max = value['max']
        return luminous_intensity
