from partcatalog.models.bridge_rectifier import BridgeRectifier
from ..json_importer_base import ModelImporter, GenerateDescriptionPolicy
from ..fields_decoder.breakdown_voltage_decoder import breakdown_voltage_decoder
from ..fields_decoder.total_capacitance_decoder import total_capacitance_decoder
from ..fields_decoder.reverse_current_decoder import reverse_current_decoder
from ..fields_decoder.forward_voltage_decoder import forward_voltage_decoder
from ..fields_decoder.current_decoder import current_at_temp_decoder
from ..fields_decoder.thermal_resistance_decoder import thermal_resistance_decoder
from ..fields_decoder.voltage_decoder import voltage_decoder


class BridgeRectifierJsonImporter(ModelImporter):
    def __init__(self):
        super().__init__(BridgeRectifier,
                         part_type=['Bridge Rectifier'],
                         generate_description=GenerateDescriptionPolicy.AlwaysGenerateDescription)
        self.parameters = {'repetitive_peak_reverse_voltage': {'decoder': voltage_decoder,
                                                               'json_field': 'V_RRM Peak Repetitive Reverse Voltage'},
                           'working_peak_reverse_voltage': {'decoder': voltage_decoder,
                                                            'json_field': 'V_RWM Working Peak Reverse Voltage'},
                           'dc_blocking_voltage': {'decoder': voltage_decoder,
                                                   'json_field': 'V_R DC Blocking Voltage'},
                           'rms_blocking_voltage': {'decoder': voltage_decoder,
                                                    'json_field': 'V_R(RMS) RMS Reverse Voltage'},
                           'average_rectified_current': {'decoder': current_at_temp_decoder,
                                                         'json_field': 'I_O Average Rectified Output Current'},
                           'thermal_resistance_junction_to_ambient_per_element': {'decoder': thermal_resistance_decoder,
                                                                                  'json_field': 'R_θJA Thermal Resistance, Junction to Ambient'},
                           'thermal_resistance_junction_to_case_per_element': {'decoder': thermal_resistance_decoder,
                                                                               'json_field': 'R_θJC  Thermal Resistance, Junction to Case'},
                           'thermal_resistance_junction_to_lead_per_element': {'decoder': thermal_resistance_decoder,
                                                                               'json_field': 'R_θJL Thermal Resistance, Junction to Lead'},
                           'reverse_breakdown_voltage': {'decoder': breakdown_voltage_decoder,
                                                         'json_field': 'V_(BR)R Reverse Breakdown Voltage'},
                           'forward_voltage_per_element': {'decoder': forward_voltage_decoder,
                                                           'json_field': 'V_F Forward Voltage (per element)'},
                           'leakage_current_per_element': {'decoder': reverse_current_decoder,
                                                           'json_field': 'I_R Leakage Current (per element)'},
                           'total_capacitance_per_element': {'decoder': total_capacitance_decoder,
                                                             'json_field': 'C_T Total Capacitance (per element)'}
                           }
