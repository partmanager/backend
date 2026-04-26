from partcatalog.models.others.threeDFilament import Filament, FilamentTypes
from partcatalog.importers.json_product_importer import ProductImporter, GenerateDescriptionPolicy


def char_decoder(value):
    return value

def float_decoder(value):
    return float(value)


class FilamentJsonImporter(ProductImporter):
    def __init__(self):
        super().__init__(Filament, part_type=['3DFilament'], generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'material': {'decoder': FilamentTypes.from_string, 'json_field': 'material'},
                           'color': {'decoder': char_decoder, 'json_field': 'color'},
                           'weight': {'decoder': float_decoder, 'json_field': 'weight'}
                           }
        self.parameters_todo.append('diameter')
        self.parameters_todo.append("young'sMod")