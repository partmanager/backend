from partcatalog.models.transistor_mosfet import TransistorMosfet
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy


class TransistorMosfetJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(TransistorMosfet,
                         part_type=['Transistor MOSFET N', 'Transistor MOSFET P'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {}

        self.parameters_todo.add('Drain Source Breakdown Voltage')
        self.parameters_todo.add('Forward Transconductance')
