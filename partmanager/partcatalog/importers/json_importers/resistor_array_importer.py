from partcatalog.models.resistor_array import ResistorArray
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_voltage_decoder import max_voltage_decoder
from ..fields_decoder.max_power_decoder import max_power_decoder
from ..fields_decoder.resistance_decoder import resistance_decoder
from ..fields_decoder.int_decoder import int_decoder


class ResistorArrayJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(ResistorArray,
                         part_type=['Resistor Array'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'elements_count': {'decoder': int_decoder, 'json_field': 'Elements Count'},
                           'resistance': {'decoder': resistance_decoder, 'json_field': 'Resistance'},
                           'power_rating_per_resistor': {'decoder': max_power_decoder, 'json_field': 'Power Rating Per Resistor'},
                           'power_rating_package': {'decoder': max_power_decoder, 'json_field': 'Power Rating Package'},
                           'working_voltage': {'decoder': max_voltage_decoder,
                                                   'json_field': 'Working Voltage'},
                           'overload_voltage': {'decoder': max_voltage_decoder,
                                                    'json_field': 'Overload Voltage'},
                           }
        self.parameters_todo.add('TCR')
