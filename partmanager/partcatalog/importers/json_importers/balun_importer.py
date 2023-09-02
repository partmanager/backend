from partcatalog.models.balun import Balun
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.decibel_decoder import decibel_decoder
from ..fields_decoder.frequency_range_decoder import frequency_range_decoder
from ..fields_decoder.impedance_decoder import impedance_at_freq_decoder
from ..fields_decoder.phase_decoder import phase_decoder
from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.return_loss_decoder import return_loss_decoder


class BalunJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Balun, part_type=['Balun'], generate_description=GenerateDescriptionPolicy.AlwaysUseFileDescription)
        self.parameters = {'technology': {'decoder': Balun.Technology.from_string, 'json_field': 'Technology'},
                           'operating_frequency_range': {'decoder': frequency_range_decoder, 'json_field': 'Operating Frequency Range'},
                           'unbalanced_port_impedance': {'decoder': impedance_at_freq_decoder, 'json_field': 'Unbalanced Port Impedance'},
                           'balanced_port_impedance': {'decoder': impedance_at_freq_decoder, 'json_field': 'Balanced Port Impedance'},
                           'unbalanced_port_return_loss': {'decoder': return_loss_decoder, 'json_field': 'Unbalanced Port Return Loss'},
                           'phase_balance': {'decoder': phase_decoder, 'json_field': 'Phase Balance'},
                           'amplitude_balance': {'decoder': decibel_decoder, 'json_field': 'Amplitude Balance'},
                           'insertion_loss': {'decoder': decibel_decoder, 'json_field': 'Insertion Loss'},
                           'power_rating': {'decoder': power_decoder, 'json_field': 'Power Rating'}
                           }
