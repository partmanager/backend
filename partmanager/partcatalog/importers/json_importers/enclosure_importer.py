from partcatalog.models.enclosure import Enclosure
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.dimension_decoder import dimension_decoder


class EnclosureJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Enclosure,
                         part_type=['Enclosure', 'Enclosure Accessory'],
                         generate_description=GenerateDescriptionPolicy.AlwaysUseFileDescription)
        self.parameters = {'material': {'decoder': Enclosure.Material.from_string, 'json_field': 'Material'},
                           'color': {'decoder': Enclosure.Color.from_string, 'json_field': 'Color'},
                           'flame_rating': {'decoder': Enclosure.FlameRating.from_string, 'json_field': 'Flame Rating'},
                           'ip_rating': {'decoder': Enclosure.IPRating.from_string, 'json_field': 'IP Rating'},
                           'length': {'decoder': dimension_decoder, 'json_field': 'Length'},
                           'width': {'decoder': dimension_decoder, 'json_field': 'Width'},
                           'height': {'decoder': dimension_decoder, 'json_field': 'Height'},
                           'pcb_length': {'decoder': dimension_decoder, 'json_field': 'PCB Length'},
                           'pcb_width': {'decoder': dimension_decoder, 'json_field': 'PCB Width'}
                           }
        self.parameters_todo.add('Enclosure Type')
