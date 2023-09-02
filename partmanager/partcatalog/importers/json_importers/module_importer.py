from partcatalog.models.module import Module
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy


class ModuleJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Module,
                         part_type=['Module'],
                         generate_description=GenerateDescriptionPolicy.AlwaysUseFileDescription)
        self.parameters = {'category': {'decoder': Module.ModuleCategory.from_str, 'json_field': 'Module Type'}
                           }
        self.parameters_todo.add('Frequency')
        self.parameters_todo.add('Key')
