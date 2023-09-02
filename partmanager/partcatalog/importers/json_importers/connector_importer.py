import decimal
from partcatalog.models.connector import Connector
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.int_decoder import int_decoder


def decode_mm_distance(json_data):
    if json_data['value']:
        return decimal.Decimal(json_data['value'].replace('mm', ''))


class ConnectorJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Connector,
                         part_type=['Connector', 'Connector IDC', 'Connector Bus', 'Connector Terminal Block',
                                    'Connector microSD Card', 'Connector FFC/FPC', 'Connector Accessory', 'Connector Pins'],
                         generate_description=GenerateDescriptionPolicy.GenerateDescriptionIfMissing)
        self.parameters = {'contact_position': {'decoder': Connector.ContactPositionChoices.from_string, 'json_field': 'Contact Position'},
                           'bus_type': {'decoder': Connector.bus_from_str, 'json_field': 'Bus Type'},
                           'pin_count': {'decoder': int_decoder, 'json_field': 'Pin Count'},
                           'row_count': {'decoder': int_decoder, 'json_field': 'Row Count'},
                           'pin_spacing': {'decoder': decode_mm_distance, 'json_field': 'Pin Spacing'},
                           'row_spacing': {'decoder': decode_mm_distance, 'json_field': 'Row Spacing'},
                           'pin_height': {'decoder': decode_mm_distance, 'json_field': 'Pin Height'},
                           'pin_height_form_pcb': {'decoder': decode_mm_distance, 'json_field': 'Pin Height from PCB'},
                           'housing_height': {'decoder': decode_mm_distance, 'json_field': 'Housing Height'}
                           }
        self.parameters_todo.add('Rated Current')
        self.parameters_todo.add('Contact Resistance')
        self.parameters_todo.add('Height from PCB')
        self.parameters_todo.add('Rated Voltage')
        self.parameters_todo.add('Wire Range')
