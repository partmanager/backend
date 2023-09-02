from partcatalog.models.relay import Relay
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.insulation_resistance_decoder import insulation_resistance_decoder
from ..fields_decoder.resistance_decoder import resistance_decoder
from ..fields_decoder.max_voltage_decoder import max_voltage_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder
from ..fields_decoder.int_decoder import int_decoder


class RelayJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Relay,
                         part_type=['Relay'],
                         generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'coil_voltage': {'decoder': voltage_decoder, 'json_field': 'Coil Voltage'},
                          # 'coil_must_release_voltage': {'decoder': max_voltage_decoder, 'json_field': 'Coil Must Release Voltage'},
                           'coil_resistance': {'decoder': resistance_decoder, 'json_field': 'Coil Resistance'},
                           'coil_power': {'decoder': power_decoder, 'json_field': 'Coil Power'},
                           'configuration': {'decoder': Relay.ConfigurationChoices.from_string,
                                             'json_field': 'Contact Configuration'},
                           'switching_voltage': {'decoder': voltage_decoder, 'json_field': 'Switching Voltage'},
                           'switching_current': {'decoder': current_at_temp_decoder, 'json_field': 'Switching Current'},
                           'contact_resistance': {'decoder': resistance_decoder, 'json_field': 'Contact Resistance'},
                           'operating_life': {'decoder': int_decoder, 'json_field': 'Contact Operating Life'},
                           'insulation_resistance': {'decoder': insulation_resistance_decoder,
                                                     'json_field': 'Insulation Resistance'}
                           }
        self.parameters_todo.add('Coil Must Release Voltage')
        self.parameters_todo.add('Operating time')
        self.parameters_todo.add('Release time')
