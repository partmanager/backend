from partcatalog.models.fuse import Fuse
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_current_decoder import max_current_at_temp_decoder
from ..fields_decoder.max_voltage_decoder import max_voltage_at_temp_decoder
from ..fields_decoder.melting_integral_decoder import melting_integral_decoder
from ..fields_decoder.time_at_current_decoder import time_at_current_decoder


class FuseJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Fuse, part_type=['Fuse'], generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'rated_current': {'decoder': max_current_at_temp_decoder, 'json_field': 'Rated Current'},
                           'rated_voltage': {'decoder': max_voltage_at_temp_decoder, 'json_field': 'Rated Voltage'},
                           'breaking_capacity': {'decoder': max_current_at_temp_decoder, 'json_field': 'Breaking Capacity'},
                           'voltage_drop': {'decoder': max_voltage_at_temp_decoder, 'json_field': 'Voltage Drop'},
                           'melting_integral': {'decoder': melting_integral_decoder, 'json_field': 'Melting Integral'}
                           }
