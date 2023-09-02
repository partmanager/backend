from partcatalog.models.common_mode_choke import CommonModeChoke
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.impedance_decoder import impedance_at_freq_decoder
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.resistance_decoder import resistance_decoder


class CommonModeChokeJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(CommonModeChoke, part_type=['Common Mode Choke'], generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'impedance': {'decoder': impedance_at_freq_decoder, 'json_field': 'Impedance',
                                         'max_values_count': CommonModeChoke.impedance_max_values_count},
                           'dc_rated_current': {'decoder': current_at_temp_decoder, 'json_field': 'Rated Current',
                                                'max_values_count': CommonModeChoke.dc_rated_current_max_values_count},
                           'dc_resistance': {'decoder': resistance_decoder, 'json_field': 'DC Resistance'}
                           }
