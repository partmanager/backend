from .part import Part
from composite_field import CompositeField
from django.db import models


class DrainSourceBreakdown(CompositeField):
    symbol = 'V_(BR)DS'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class Gate1SourceBreakdownVoltage(CompositeField):
    symbol = 'V_(BR)B1SS'
    symbol_html = 'V_(BR)B1SS'
    min = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class Gate2SourceBreakdownVoltage(CompositeField):
    symbol = 'V_(BR)B2SS'
    symbol_html = 'V_(BR)B2SS'
    min = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class GateSourceLeakageCurrent(CompositeField):
    symbol = 'I_GxSS'
    symbol_html = 'I_GxSS'
    min = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class DrainCurrent(CompositeField):
    symbol = 'I_DSS'
    symbol_html = 'I_DSS'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class Gate1SourcePinchOffVoltage(CompositeField):
    symbol = 'V_G1S(p)'
    symbol_html = 'V_G1S(p)'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class Gate2SourcePinchOffVoltage(CompositeField):
    symbol = 'V_G2S(p)'
    symbol_html = 'V_G2S(p)'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate1_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class ForwardTransconductance(CompositeField):
    symbol = 'g_fs'
    symbol_html = 'g_fs'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)


class Gate1InputCapacitance(CompositeField):
    symbol = 'C_g1ss'
    symbol_html = 'C_g1ss'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class Gate2InputCapacitance(CompositeField):
    symbol = 'C_g2ss'
    symbol_html = 'C_g2ss'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class FeedbackCapacitance(CompositeField):
    symbol = 'C_dg1'
    symbol_html = 'C_dg1'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class OutputCapacitance(CompositeField):
    symbol = 'C_dg1'
    symbol_html = 'C_dg1'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class PowerGain(CompositeField):
    symbol = 'G_p'
    symbol_html = 'G_p'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class NoiseFigure(CompositeField):
    symbol = 'F'
    symbol_html = 'F'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class GainControlRange(CompositeField):
    symbol = '∆G_p'
    symbol_html = '∆G_p'
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_drain_source_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_min_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_gate2_source_max_voltage = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)


class TransistorMosfet(Part):
    part_type_subset = ['TMP', 'TMN']
    # DC Characteristics
    drain_source_breakdown_voltage = DrainSourceBreakdown()
    gate1_source_breakdown_voltage = Gate1SourceBreakdownVoltage()
    gate2_source_breakdown_voltage = Gate2SourceBreakdownVoltage()
    gate1_source_leakage_current = GateSourceLeakageCurrent()
    gate2_source_leakage_current = GateSourceLeakageCurrent()
    drain_current = DrainCurrent()
    gate1_source_pinch_off_voltage = Gate1SourcePinchOffVoltage()
    gate2_source_pinch_off_voltage = Gate2SourcePinchOffVoltage()
    # AC Characteristics
    forward_transconductance = ForwardTransconductance()
    gate1_input_capacitance = Gate1InputCapacitance()
    gate2_input_capacitance = Gate2InputCapacitance()
    feedback_capacitance = FeedbackCapacitance()
    output_capacitance = OutputCapacitance()
    power_gain_1 = PowerGain()
    power_gain_2 = PowerGain()
    power_gain_3 = PowerGain()
    noise_figure_1 = NoiseFigure()
    noise_figure_2 = NoiseFigure()
    noise_figure_3 = NoiseFigure()
    gain_control_range = GainControlRange()

    def generate_description(self):
        return f"MOSFET N, {self.drain_source_breakdown_voltage}"
