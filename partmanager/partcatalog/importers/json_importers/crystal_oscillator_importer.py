from partcatalog.models.crystal_oscillator import CrystalOscillator
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.time_decoder import time_decoder, fall_time_decoder, rise_time_decoder, bool_decoder,\
    frequency_decoder, supply_voltage_range_decoder, supply_current_range_decoder, frequency_stability_decoder
from ..fields_decoder.supply_current_range_decoder import supply_current_range_decoder
from ..fields_decoder.frequency_decoder import frequency_decoder
from ..fields_decoder.frequency_stability_decoder import frequency_stability_decoder
from ..fields_decoder.ageing_decoder import ageing_decoder


class CrystalOscillatorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(CrystalOscillator,
                         part_type=['Crystal Oscillator'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'frequency': {'decoder': frequency_decoder, 'json_field': 'Frequency'},
                           'supply_voltage': {'decoder': supply_voltage_range_decoder, 'json_field': 'Supply Voltage'},
                           'supply_current': {'decoder': supply_current_range_decoder, 'json_field': 'Supply Current'},
                           'standby_current': {'decoder': supply_current_range_decoder, 'json_field': 'Stand-by Current'},
                           'frequency_stability_over_operating_temperature_range': {'decoder': frequency_stability_decoder, 'json_field': 'Frequency Stability Over Operating Temperature Range'},
                           'rise_time': {'decoder': rise_time_decoder, 'json_field': 'Rise Time'},
                           'fall_time': {'decoder': fall_time_decoder, 'json_field': 'Fall Time'},
                           'startup_time': {'decoder': time_decoder, 'json_field': 'Start-up Time'},
                           'peak_to_peak_jitter': {'decoder': time_decoder, 'json_field': 'Peak to Peak Jitter'},
                           'rms_jitter': {'decoder': time_decoder, 'json_field': 'RMS Jitter'},
                           'ageing': {'decoder': ageing_decoder, 'json_field': 'Ageing'},
                           'enable_pin': {'decoder': bool_decoder, 'json_field': 'Enable pin'},
                           'tri_state_output': {'decoder': bool_decoder, 'json_field': 'Tri-state Output'}}
        self.parameters_todo.add('Output Load')
