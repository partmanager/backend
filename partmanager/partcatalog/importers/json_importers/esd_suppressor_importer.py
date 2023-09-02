from partcatalog.models.esd_suppressor import ESDSuppressor
from partcatalog.importers.json_importer_base import ModelImporter, GenerateDescriptionPolicy
from partcatalog.importers.fields_decoder.capacitance_decoder import capacitance_at_frequency_decoder
from partcatalog.importers.fields_decoder.current_decoder import current_at_temp_decoder
from partcatalog.importers.fields_decoder.voltage_decoder import voltage_decoder
from partcatalog.importers.fields_decoder.decibel_decoder import decibel_decoder
from ..fields_decoder.decimal_decoder import decimal_decoder


class ESDSuppressorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(ESDSuppressor,
                         part_type=['ESD Suppressor'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'rated_voltage': {'decoder': voltage_decoder, 'json_field': 'Rated Voltage'},
                           'clamping_voltage': {'decoder': voltage_decoder, 'json_field': 'Clamping Voltage'},
                           'trigger_voltage': {'decoder': voltage_decoder, 'json_field': 'Trigger Voltage'},
                           'capacitance': {'decoder': capacitance_at_frequency_decoder, 'json_field': 'Capacitance'},
                           'attenuation': {'decoder': decibel_decoder, 'json_field': 'Attenuation'},
                           'leakage_current': {'decoder': current_at_temp_decoder, 'json_field': 'Leakage Current'},
                           'esd_pulse_withstand_count': {'decoder': decimal_decoder, 'json_field': 'ESD pulse withstand'}}
        self.parameters_todo.add('Directions')