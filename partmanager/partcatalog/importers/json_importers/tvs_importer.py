from partcatalog.models.diode import TVS
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy

from ..fields_decoder.breakdown_voltage_decoder import breakdown_voltage_decoder
from ..fields_decoder.clamping_voltage_decoder import clamping_voltage_decoder

from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.max_current_decoder import max_current_at_temp_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder


class TVSJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(TVS,
                         part_type=['TVS'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'configuration': {'decoder': TVS.configuration_from_str, 'json_field': 'Configuration'},
                           'reverse_standoff_voltage': {'decoder': voltage_decoder, 'json_field': 'V_RWM'},
                           'breakdown_voltage': {'decoder': breakdown_voltage_decoder, 'json_field': 'V_BR'},
                           'clamping_voltage': {'decoder': clamping_voltage_decoder, 'json_field': 'V_CL',
                                                'max_values_count': 2},
                           'peak_pulse_current_max': {'decoder': max_current_at_temp_decoder, 'json_field': 'IPP'},
                           'power_rating': {'decoder': power_decoder, 'json_field': 'Power Rating'},
                           }
        self.parameters_todo.add('I_RM')
        self.parameters_todo.add('I_R')
        self.parameters_todo.add('Cd')
        self.parameters_todo.add('V_ESD MIL-STD-883')
        self.parameters_todo.add('V_ESD IEC 61000-4-2')
        self.parameters_todo.add('V_ESD machine model')
