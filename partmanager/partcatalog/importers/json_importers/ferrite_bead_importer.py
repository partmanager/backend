from partcatalog.models.ferrite_bead import FerriteBead
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.impedance_decoder import impedance_at_freq_decoder
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.resistance_decoder import resistance_at_temp_decoder


class FerriteBeadJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(FerriteBead,
                         part_type=['Ferrite Bead'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'impedance': {'decoder': impedance_at_freq_decoder, 'json_field': 'Impedance',
                                         'max_values_count': FerriteBead.impedance_max_values_count},
                           'dc_rated_current': {'decoder': current_at_temp_decoder, 'json_field': 'Rated Current',
                                                'max_values_count': FerriteBead.dc_rated_current_max_values_count},
                           'dc_resistance': {'decoder': resistance_at_temp_decoder, 'json_field': 'DC Resistance'}
                           }
