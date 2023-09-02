from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from partcatalog.models.inductor import Inductor
from partcatalog.importers.fields_decoder.resistance_decoder import resistance_at_temp_decoder
from partcatalog.importers.fields_decoder.current_decoder import current_at_temp_decoder
from partcatalog.importers.fields_decoder.decimal_decoder import decimal_decoder
from partcatalog.importers.fields_decoder.self_resonant_frequency_decoder import self_resonant_frequency_decoder
from partcatalog.importers.fields_decoder.dc_saturation_current_decoder import dc_saturation_current_decoder
from partcatalog.importers.fields_decoder.q_factor_decoder import q_factor_decoder
from partcatalog.importers.fields_decoder.inductance_decoder import inductance_at_frequency_at_temp_decoder
from partcatalog.importers.fields_decoder.voltage_decoder import voltage_decoder


class InductorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Inductor, part_type=['Inductor'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'inductance': {'decoder': inductance_at_frequency_at_temp_decoder, 'json_field': 'Inductance'},
                           #'inductance_tolerance': {'decoder': supply_voltage_range_decoder, 'json_field': 'Inductance'},
                           'dc_resistance': {'decoder': resistance_at_temp_decoder, 'json_field': 'DCR'},
                           'dc_rated_current': {'decoder': current_at_temp_decoder, 'json_field': 'DC Rated Current'},
                           'q_factor': {'decoder': q_factor_decoder, 'json_field': 'Q'},
                           'dc_saturation_current': {'decoder': dc_saturation_current_decoder,
                                                     'json_field': 'DC Saturation Current',
                                                     'max_values_count': Inductor.dc_saturation_current_max_values_count},
                           'srf': {'decoder': self_resonant_frequency_decoder, 'json_field': 'SRF'},
                           'rated_operating_voltage': {'decoder': voltage_decoder, 'json_field': 'Rated Operating Voltage'}
                           }
        self.parameters_todo.add('Heat Reating Current')
