from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from partcatalog.models.integrated_circuit import IntegratedCircuit
from partcatalog.importers.fields_decoder.supply_voltage_range_decoder import supply_voltage_range_decoder


class IntegratedCircuitJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(IntegratedCircuit, part_type=['IC',
                                                       'IC ADC',
                                                       'IC DAC',
                                                       'IC Opamp',
                                                       'IC RF Synthesizer',
                                                       'IC RF Amplifier',
                                                       'IC Voltage Regulator',
                                                       'IC Voltage Reference',
                                                       "IC Current Sense",
                                                       "IC Comparator",
                                                       "IC Voltage Regulator Switching",
                                                       "IC LDO",
                                                       "IC Sensor",
                                                       "IC MCU",
                                                       "IC Load Switch",
                                                       "IC Level translator"],
                         generate_description=GenerateDescriptionPolicy.AlwaysUseFileDescription)
        self.parameters = {'supply_voltage': {'decoder': supply_voltage_range_decoder, 'json_field': 'Supply Voltage Range'}
                           }
        self.parameters_todo.add('Frequency')
        self.parameters_todo.add('Supply Voltage 2 Range')
