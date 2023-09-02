from partcatalog.models.diode import Diode
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.breakdown_voltage_decoder import breakdown_voltage_decoder
from ..fields_decoder.junction_capacitance_decoder import junction_capacitance_decoder
from ..fields_decoder.power_decoder import power_decoder
from ..fields_decoder.forward_voltage_decoder import forward_voltage_decoder
from ..fields_decoder.current_decoder import current_decoder
from ..fields_decoder.time_decoder import time_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder
from ..fields_decoder.reverse_current_decoder import reverse_current_decoder


class DiodeJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(Diode,
                         part_type=['Small Signal Diode', 'Schottky Diode'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'forward_voltage': {'decoder': forward_voltage_decoder,
                                               'json_field': 'Forward Voltage', 'max_values_count': 4},
                           'reverse_current': {'decoder': reverse_current_decoder,
                                               'json_field': 'Reverse Current', 'max_values_count': Diode.reverse_current_max_values_count},
                           'capacitance_in_pf': {'decoder': junction_capacitance_decoder,
                                                 'json_field': 'Junction Capacitance'},
                           'forward_continuous_current': {'decoder': current_decoder,
                                                          'json_field': 'I_F'},
                           'repetitive_peak_forward_current': {'decoder': current_decoder, 'json_field': 'I_FRM'},
                           'peak_forward_surge_current': {'decoder': current_decoder, 'json_field': 'I_FSM'},
                           'power_rating': {'decoder': power_decoder, 'json_field': 'Power Rating'},
                           'breakdown_voltage': {'decoder': breakdown_voltage_decoder, 'json_field': 'V_BR'},
                           'reverse_recovery_time_in_ns': {'decoder': time_decoder, 'json_field': 't_rr'},
                           'repetitive_peak_reverse_voltage': {'decoder': voltage_decoder, 'json_field': 'V_RRM'},
                           'reverse_voltage': {'decoder': voltage_decoder, 'json_field': 'V_R'}
                           }
        self.parameters_todo.add('V_RSM')
