from .part import Part
from .fields.breakdown_voltage import BreakdownVoltage
from .fields.current import CurrentAtTemp
from .fields.forward_voltage import ForwardVoltage
from .fields.reverse_current import ReverseCurrent
from .fields.thermal_resistance import ThermalResistance
from .fields.total_capacitance import TotalCapacitance
from .fields.voltage import Voltage


class BridgeRectifier(Part):
    part_type_subset = ['BRG']
    repetitive_peak_reverse_voltage = Voltage()  # V_RRM
    working_peak_reverse_voltage = Voltage()  # V_RWM
    dc_blocking_voltage = Voltage()  # V_R DC
    rms_blocking_voltage = Voltage()  # V_R RMS
    average_rectified_current = CurrentAtTemp()  # I_O
    # Thermal characteristics
    thermal_resistance_junction_to_ambient_per_element = ThermalResistance()  # R_θJA
    thermal_resistance_junction_to_case_per_element = ThermalResistance()  # R_θJC
    thermal_resistance_junction_to_lead_per_element = ThermalResistance()  # R_θJL
    # Electrical Characteristics
    reverse_breakdown_voltage = BreakdownVoltage()  # V_(BR)R
    forward_voltage_per_element = ForwardVoltage()  # V_F
    leakage_current_per_element = ReverseCurrent()  # I_R
    total_capacitance_per_element = TotalCapacitance()  # C_T

    def generate_description(self):
        return "Bridge Rectifier {}, {}".format(self.average_rectified_current, self.reverse_breakdown_voltage)
