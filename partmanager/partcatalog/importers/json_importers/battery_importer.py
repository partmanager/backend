from partcatalog.models.battery import Battery, BatteryType, BatteryClassification
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.voltage_decoder import voltage_decoder
from ..fields_decoder.resistance_decoder import resistance_at_temp_decoder
from ..fields_decoder.battery_capacity_decoder import battery_capacity_decoder


class BatteryJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Battery, part_type=['Battery'], generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'battery_type': {'decoder': BatteryType.from_string, 'json_field': 'Battery Type'},
                           'classification': {'decoder': BatteryClassification.from_string, 'json_field': 'Battery Classification'},
                           'nominal_voltage': {'decoder': voltage_decoder, 'json_field': 'Nominal Voltage'},
                           'internal_resistance': {'decoder': resistance_at_temp_decoder, 'json_field': 'Nominal Internal Resistance'},
                           'capacity': {'decoder': battery_capacity_decoder, 'json_field': 'Capacity', 'max_values_count': Battery.capacity_max_values_count}
                           }
