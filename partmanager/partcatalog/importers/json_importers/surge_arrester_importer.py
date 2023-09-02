from partcatalog.models.surge_arrester import SurgeArrester
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.capacitance_decoder import capacitance_at_frequency_decoder
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.insulation_resistance_decoder import insulation_resistance_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder


class SurgeArresterJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(SurgeArrester,
                         part_type=['Surge arrester'],
                         generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'dc_spark_over_voltage': {'decoder': voltage_decoder, 'json_field': 'DC Spark-Over Voltage'},
                           'arc_voltage': {'decoder': voltage_decoder, 'json_field': 'Arc voltage'},
                           'glow_voltage': {'decoder': voltage_decoder, 'json_field': 'Glow voltage'},
                           'glow_to_arc_transition_current': {'decoder': current_at_temp_decoder, 'json_field': 'Arc to glow transition'},
                           'insulation_resistance': {'decoder': insulation_resistance_decoder, 'json_field': 'Insulation Resistance'},
                           'capacitance': {'decoder': capacitance_at_frequency_decoder, 'json_field': 'Capacitance'}
                           }
