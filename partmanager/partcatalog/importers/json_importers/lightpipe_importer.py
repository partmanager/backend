from partcatalog.models.lightpipe import Lightpipe
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.dimension_decoder import dimension_decoder
from ..fields_decoder.int_decoder import int_decoder


class LightpipeJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Lightpipe,
                         part_type=['Lightpipe'],
                         generate_description=GenerateDescriptionPolicy.AlwaysUseFileDescription)
        self.parameters = {'shape': {'decoder': Lightpipe.ShapeType.from_string, 'json_field': 'Shape'},
                           'color': {'decoder': Lightpipe.Color.from_string, 'json_field': 'Color'},
                           'light_count': {'decoder': int_decoder, 'json_field': 'Lights Count'},
                           'length': {'decoder': dimension_decoder, 'json_field': 'Length'},
                           'panel_cutout_diameter': {'decoder': dimension_decoder, 'json_field': 'Panel Cutout Diameter'}
                           }
