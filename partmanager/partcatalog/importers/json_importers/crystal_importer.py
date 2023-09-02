from partcatalog.models.crystal import Crystal
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.capacitance_decoder import capacitance_decoder
from ..fields_decoder.time_decoder import frequency_decoder, frequency_stability_decoder
from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.resistance_decoder import resistance_decoder
from ..fields_decoder.frequency_decoder import frequency_decoder
from ..fields_decoder.frequency_stability_decoder import frequency_stability_decoder
from ..fields_decoder.ageing_decoder import ageing_decoder
from ..fields_decoder.insulation_resistance_decoder import insulation_resistance_decoder


class CrystalJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Crystal,
                         part_type=['Crystal'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'frequency': {'decoder': frequency_decoder, 'json_field': 'Frequency'},
                           'frequency_stability_over_operating_temperature_range': {'decoder': frequency_stability_decoder, 'json_field': 'Frequency Stability Over Operating Temperature Range'},
                           'vibration_mode': {'decoder': Crystal.vibration_mode_from_str, 'json_field': 'Vibration Mode'},
                           'load_capacitance': {'decoder': capacitance_decoder, 'json_field': 'Load Capacitance'},
                           'shunt_capacitance': {'decoder': capacitance_decoder, 'json_field': 'Shunt Capacitance'},
                           'esr': {'decoder': resistance_decoder, 'json_field': 'ESR'},
                           'drive_level': {'decoder': power_decoder, 'json_field': 'Drive Level'},
                           'ageing': {'decoder': ageing_decoder, 'json_field': 'Ageing'},
                           'insulation_resistance': {'decoder': insulation_resistance_decoder, 'json_field': 'Insulation Resistance'}
                           }
