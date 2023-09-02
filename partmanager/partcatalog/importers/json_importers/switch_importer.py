from partcatalog.models.switch import Switch
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_voltage_decoder import max_voltage_decoder
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.resistance_decoder import resistance_at_temp_decoder
from ..fields_decoder.insulation_resistance_decoder import insulation_resistance_decoder
from ..fields_decoder.int_decoder import int_decoder
from ..fields_decoder.dimension_decoder import dimension_decoder


class SwitchJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Switch,
                         part_type=['Switch'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'switch_type': {'decoder': Switch.SwitchType.from_string, 'json_field': 'Switch Type'},
                           'configuration': {'decoder': Switch.ConfigurationChoices.from_string, 'json_field': 'Configuration'},
                           'position_count': {'decoder': int_decoder,
                                              'json_field': 'Position Count'},
                           'pin_pitch': {'decoder': dimension_decoder, 'json_field': 'Pin Pitch'},
                           'switching_voltage': {'decoder': max_voltage_decoder,
                                                 'json_field': 'Switching Voltage'},
                           'switching_current': {'decoder': current_at_temp_decoder,
                                                 'json_field': 'Switching Current'},
                           'contact_resistance': {'decoder': resistance_at_temp_decoder,
                                                  'json_field': 'Contact Resistance'},
                           'insulation_resistance': {'decoder': insulation_resistance_decoder,
                                                     'json_field': 'Insulation Resistance'},
                           'operating_life': {'decoder': int_decoder,
                                              'json_field': 'Operating Life'},
                           }
