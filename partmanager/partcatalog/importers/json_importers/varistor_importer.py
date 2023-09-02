from partcatalog.models.varistor import Varistor
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.clamping_voltage_decoder import clamping_voltage_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder
#from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.si_unit_decoder import power_decode


class VaristorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Varistor,
                         part_type=['Varistor'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'voltage': {'decoder': voltage_decoder,
                                               'json_field': 'Varistor Voltage'},
                           'rated_rms_voltage': {'decoder': voltage_decoder,
                                       'json_field': 'RMS Voltage'},
                           'rated_dc_voltage': {'decoder': voltage_decoder,
                                       'json_field': 'DC Voltage'},
                           'clamping_voltage': {'decoder': clamping_voltage_decoder, 'json_field': 'Clamping Voltage'},
                           'power_rating': {'decoder': power_decode, 'json_field': 'Power Rating'}
                           }
