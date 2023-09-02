from partcatalog.models.ptc_fuse import PTCFuse
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_current_decoder import max_current_at_temp_decoder
from ..fields_decoder.max_voltage_decoder import max_voltage_at_temp_decoder
from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.resistance_decoder import resistance_at_temp_decoder, resistance_decoder
from ..fields_decoder.time_at_current_decoder import time_at_current_decoder


class PTCFuseJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(PTCFuse,
                         part_type=['PTC Fuse'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'hold_current': {'decoder': max_current_at_temp_decoder, 'json_field': 'Hold Current'},
                           'trip_current': {'decoder': max_current_at_temp_decoder, 'json_field': 'Trip Current'},
                           'rated_voltage': {'decoder': max_voltage_at_temp_decoder, 'json_field': 'Rated Voltage'},
                           'fault_current': {'decoder': max_current_at_temp_decoder, 'json_field': 'Max fault current'},
                           'tripped_power_dissipation': {'decoder': power_decoder, 'json_field': 'Tripped Power Dissipation'},
                           'time_to_trip': {'decoder': time_at_current_decoder, 'json_field': 'Trip time'},
                           'resistance': {'decoder': resistance_at_temp_decoder, 'json_field': 'Resistance'},
                           'tripped_resistance': {'decoder': resistance_decoder, 'json_field': 'Resistance 1h after tripping'}
                           }
