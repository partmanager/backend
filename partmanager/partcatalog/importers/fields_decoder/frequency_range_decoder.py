from partcatalog.models.fields.frequency_range import FrequencyRange
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import frequency_decode as __frequency_decode


def frequency_range_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __frequency_decode)
    if value:
        frequency = FrequencyRange()
        frequency.min = value['min']
        frequency.max = value['max']
        return frequency
