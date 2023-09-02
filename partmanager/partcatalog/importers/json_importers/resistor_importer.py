from partcatalog.models.resistor import Resistor
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.max_power_decoder import max_power_decoder
from ..fields_decoder.temperature_coefficient_decoder import temperature_coefficient_decoder
from ..fields_decoder.max_voltage_decoder import max_voltage_decoder
from ..fields_decoder.resistance_decoder import resistance_decoder


class ResistorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Resistor,
                         part_type=['Resistor Carbon Film', 'Resistor Metal Film', 'Resistor Thick Film', 'Resistor Thin Film', 'Resistor'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'resistance': {'decoder': resistance_decoder, 'json_field': 'Resistance'},
                           'power': {'decoder': max_power_decoder, 'json_field': 'Rated Power'},
                           'temperature_coefficient': {'decoder': temperature_coefficient_decoder, 'json_field': 'TCR'},
                           'working_voltage': {'decoder': max_voltage_decoder, 'json_field': 'Working Voltage'},
                           'overload_voltage': {'decoder': max_voltage_decoder,
                                                'json_field': 'Overload Voltage'},
                           'dielectric_withstanding_voltage': {'decoder': max_voltage_decoder,
                                                               'json_field': 'Dielectric Withstanding Voltage'},
                           }
