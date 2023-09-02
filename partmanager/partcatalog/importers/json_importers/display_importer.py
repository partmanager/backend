from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from partcatalog.models.display import Display
from partcatalog.importers.fields_decoder.color_decoder import color_decoder
from partcatalog.importers.fields_decoder.resolution_decoder import resolution_decoder
from partcatalog.importers.fields_decoder.controller_decoder import controller_decoder
from partcatalog.importers.fields_decoder.backlight_decoder import backlight_decoder


class DisplayJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Display, part_type=['LCD Display'],
                         generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'color': {'decoder': color_decoder, 'json_field': 'Color'},
                           'resolution': {'decoder': resolution_decoder, 'json_field': 'Resolution'},
                           'controller': {'decoder': controller_decoder, 'json_field': 'Controller'},
                           'backlight': {'decoder': backlight_decoder, 'json_field': 'Backlight'}
                           }
