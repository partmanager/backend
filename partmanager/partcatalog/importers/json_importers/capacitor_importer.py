from partcatalog.models.capacitor import Capacitor
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_current_decoder import max_current_at_temp_at_freq_decoder
from ..fields_decoder.max_voltage_decoder import max_voltage_at_temp_decoder
from ..fields_decoder.capacitance_decoder import capacitance_decoder
from ..fields_decoder.decimal_decoder import decimal_decoder

def endurance_decoder(endurance_str):
    return int(endurance_str['value'].replace('h', ''))


class CapacitorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Capacitor,
                         part_type=['Aluminium Electrolytic Capacitor', 'MLCC'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'capacitance': {'decoder': capacitance_decoder, 'json_field': 'Capacitance'},
                           'voltage': {'decoder': max_voltage_at_temp_decoder, 'json_field': 'Rated Voltage'},
                           'endurance': {'decoder': endurance_decoder, 'json_field': 'Endurance'},
                           'rated_ripple_current': {'decoder': max_current_at_temp_at_freq_decoder,
                                                    'json_field': 'Rated Ripple Current'},
                           'dissipation_factor': {'decoder': decimal_decoder,
                                                  'json_field': 'Dissipation Factor'},
                           'dielectric_type': {'decoder': Capacitor.DielectricType.from_str,
                                               'json_field': 'Dielectric Type'},
                           }
