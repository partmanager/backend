from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from partcatalog.models.led import LED
from partcatalog.importers.fields_decoder.current_decoder import current_at_temp_decoder
from partcatalog.importers.fields_decoder.forward_voltage_decoder import forward_voltage_decoder
from partcatalog.importers.fields_decoder.max_voltage_decoder import max_voltage_at_temp_decoder
from partcatalog.importers.fields_decoder.int_decoder import int_decoder
from partcatalog.importers.fields_decoder.luminous_intensity_decoder import luminous_intensity_decoder


class LEDJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(LED, part_type=['LED'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'continuous_forward_current': {'decoder': current_at_temp_decoder, 'json_field': 'IF Continuous'},
                           'peak_forward_current': {'decoder': current_at_temp_decoder, 'json_field': 'IF Peak'},
                           'forward_voltage': {'decoder': forward_voltage_decoder, 'json_field': 'VF'},
                           'luminous_intensity': {'decoder': luminous_intensity_decoder, 'json_field': 'Luminous Intensity'},
                           'viewing_angle_in_deg': {'decoder': int_decoder, 'json_field': 'Viewing Angle'},
                           'reverse_voltage': {'decoder': max_voltage_at_temp_decoder, 'json_field': 'VR'},
                           'color': {'decoder': LED.color_from_str, 'json_field': 'Color'}
                           }
        self.parameters_todo.add('I_R')
