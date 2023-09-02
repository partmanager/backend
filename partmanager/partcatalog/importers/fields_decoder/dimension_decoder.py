from partcatalog.models.fields.dimension import Dimension
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import distance_decode as __distance_decode


def dimension_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __distance_decode)
    if value:
        dimension = Dimension()
        dimension.min = value['min']
        dimension.typ = value['typ']
        dimension.max = value['max']
        return dimension
