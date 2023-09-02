from .part import Part, decimal_voltage_to_str

from django.db import models
from .fields.breakdown_voltage import BreakdownVoltage
from .fields.forward_voltage import ForwardVoltage
from .fields.junction_capacitance import JunctionCapacitance
from .fields.reverse_current import ReverseCurrent
from .fields.clamping_voltage import ClampingVoltage
from .fields.power import Power
from .fields.time import Time
from .fields.voltage import Voltage
from .fields.current import Current


class Diode(Part):
    part_type_subset = ['D', 'DS']
    forward_voltage_1 = ForwardVoltage()  # V_F @ condition1
    forward_voltage_2 = ForwardVoltage()  # V_F @ condition2
    forward_voltage_3 = ForwardVoltage()  # V_F @ condition3
    forward_voltage_4 = ForwardVoltage()  # V_F @ condition4

    reverse_current_max_values_count = 6
    reverse_current_1 = ReverseCurrent()  # I_R @ condition1
    reverse_current_2 = ReverseCurrent()  # I_R @ condition2
    reverse_current_3 = ReverseCurrent()  # I_R @ condition3
    reverse_current_4 = ReverseCurrent()  # I_R @ condition4
    reverse_current_5 = ReverseCurrent()  # I_R @ condition5
    reverse_current_6 = ReverseCurrent()  # I_R @ condition6

    capacitance_in_pf = JunctionCapacitance()  # C_D

    forward_continuous_current = Current()
    repetitive_peak_forward_current = Current()
    peak_forward_surge_current = Current()
    power_rating = Power()
    breakdown_voltage = BreakdownVoltage()
    reverse_recovery_time_in_ns = Time()
    repetitive_peak_reverse_voltage = Voltage()
    reverse_voltage = Voltage()

    custom_fields = {'Diode Type': 'part_type',
                     'IF': 'IF',
                     'Power Rating': 'power_rating',
                     'trr': 'trr',
                     'Forward Voltage': 'forward_voltage',
                     'Reverse Current': 'reverse_current',
                     'V_RRM': 'v_rrm',
                     'I_FSM': 'i_fsm',
                     'Cd': 'cd'}
    fields = {**Part.fields_begin, **custom_fields, **Part.fields_end}

    def generate_description(self):
        return "{}, {}, {}".format(self.get_part_type_display(),
                                   str(self.forward_continuous_current),
                                   str(self.repetitive_peak_reverse_voltage))

    def __str__(self):
        return self.manufacturer_part_number


class ZenerDiode(Part):
    forward_voltage = ForwardVoltage()  # V_F @ condition1
    power_rating = Power()

    def generate_description(self):
        return f"Diode Zener, {self.forward_voltage.get_display()} {self.power_rating}"


class TVS(Part):
    CONFIGURATION_TYPE = (
        ('u', 'Unidirectional'),
        ('b', 'Bidirectional')
    )
    part_type_subset = ['TVS']
    configuration = models.CharField(max_length=1, choices=CONFIGURATION_TYPE)
    reverse_standoff_voltage_in_volts = models.DecimalField(max_digits=6, decimal_places=2)  # Vrwm
    breakdown_voltage = BreakdownVoltage()
    test_current_in_mA = models.IntegerField(null=True, blank=True)  # It todo remove
    clamping_voltage = ClampingVoltage()
    clamping_voltage2 = ClampingVoltage()
    peak_pulse_current_max_in_amper = models.DecimalField(max_digits=6, decimal_places=2)  # Ipp
    reverse_leakage_current_max_in_uA = models.IntegerField(null=True, blank=True)  # Ir @ Vrwm
    power_rating_in_wats = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    custom_fields = {'Configuration': 'configuration', 'Power Rating': 'power_rating_in_wats'}
    fields = {**Part.fields_begin, **custom_fields, **Part.fields_end}

    @staticmethod
    def configuration_from_str(configuration_str):
        configuration = {"Unidirectional": 'u', "Bidirectional": 'b'}
        return configuration[configuration_str]

    def generate_description(self):
        return "TVS, {} {}".format(self.get_configuration_display(),
                                   decimal_voltage_to_str(self.reverse_standoff_voltage_in_volts))
