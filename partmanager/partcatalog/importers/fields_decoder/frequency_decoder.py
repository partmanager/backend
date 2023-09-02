from partcatalog.models.fields.frequency import Frequency
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import frequency_decode as __frequency_decode


def frequency_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __frequency_decode)
    if value:
        frequency = Frequency()
        frequency.min = value['min']
        frequency.typ = value['typ']
        frequency.max = value['max']
        frequency.tolerance_ppm = None
        frequency.at_temp = None
        frequency.at_temp_tolerance = None
        return frequency
