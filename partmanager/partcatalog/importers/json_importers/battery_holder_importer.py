from partcatalog.models.battery_holder import BatteryHolder, BatteryType
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.int_decoder import int_decoder


class BatteryHolderJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(BatteryHolder, part_type=['Battery Holder'], generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'battery_count': {'decoder': int_decoder, 'json_field': 'Battery Count'},
                           'battery_type': {'decoder': BatteryType.from_string, 'json_field': 'Battery Type'}
                           }
