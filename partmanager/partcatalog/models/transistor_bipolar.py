from .part import Part, decimal_celsius_to_str, decimal_current_to_str, decimal_voltage_to_str
from .to_string_conversions import decimal_frequency_to_str, decimal_power_to_str, decimal_capacitance_to_str
from django.db import models
from composite_field import CompositeField


class BreakdownVoltage(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_collector_current = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_voltage_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_voltage_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_voltage_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "I<sub>C</sub>={}, T<sub>A</sub>={}".format(
                decimal_current_to_str(self.at_collector_current),
                decimal_celsius_to_str(self.at_temp))


class CECutOffCurrent(CompositeField):
    min = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    at_collector_emitter_voltage = models.IntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def get_min_display(self):
            return decimal_current_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_current_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_current_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "V<sub>CE</sub>={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_collector_emitter_voltage),
                decimal_celsius_to_str(self.at_temp))


class BECutOffCurrent(CompositeField):
    min = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    typ = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    max = models.DecimalField(max_digits=9, decimal_places=9, null=True, blank=True)
    at_voltage = models.IntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None

        def get_min_display(self):
            return decimal_current_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_current_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_current_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "V<sub>EB</sub>={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_voltage),
                decimal_celsius_to_str(self.at_temp))


class DCCurrentGain(CompositeField):
    min = models.IntegerField(null=True, blank=True)
    typ = models.IntegerField(null=True, blank=True)
    max = models.IntegerField(null=True, blank=True)
    at_collector_emitter_voltage = models.IntegerField(null=True, blank=True)
    at_collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return self.min if self.min else ''

        def get_typ_display(self):
            return self.typ if self.typ else ''

        def get_max_display(self):
            return self.max if self.max else ''

        def get_condition_display(self):
            return "V<sub>CE</sub>={}, I<sub>C</sub>={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_collector_emitter_voltage),
                decimal_current_to_str(self.at_collector_current),
                decimal_celsius_to_str(self.at_temp))


class CollectorEmitterSaturationVoltage(CompositeField):
    min = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    at_base_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_voltage_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_voltage_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_voltage_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "I<sub>C</sub>={}, I<sub>B</sub>={}, T<sub>A</sub>={}".format(
                decimal_current_to_str(self.at_collector_current),
                decimal_current_to_str(self.at_base_current),
                decimal_celsius_to_str(self.at_temp))


class BaseEmitterVoltage(CompositeField):
    min = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    typ = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_collector_emitter_voltage = models.IntegerField(null=True, blank=True)
    at_collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_voltage_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_voltage_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_voltage_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "V<sub>CE</sub>={}, I<sub>C</sub>={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_collector_emitter_voltage),
                decimal_current_to_str(self.at_collector_current),
                decimal_celsius_to_str(self.at_temp))


class GainBandwidthProduct(CompositeField):
    min = models.IntegerField(null=True, blank=True)
    typ = models.IntegerField(null=True, blank=True)
    max = models.IntegerField(null=True, blank=True)
    at_collector_emitter_voltage = models.IntegerField(null=True, blank=True)
    at_collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    at_frequency = models.BigIntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_frequency_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_frequency_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_frequency_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "V<sub>CE</sub>={}, I<sub>C</sub>={}, f={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_collector_emitter_voltage),
                decimal_current_to_str(self.at_collector_current),
                decimal_frequency_to_str(self.at_frequency),
                decimal_celsius_to_str(self.at_temp))


class CollectorBaseCapacitance(CompositeField):
    min = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    typ = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    max = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    at_collector_base_voltage = models.IntegerField(null=True, blank=True)
    at_frequency = models.BigIntegerField(null=True, blank=True)
    at_temp = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def __bool__(self):
            return self.max is not None or self.typ is not None or self.min is not None

        def get_min_display(self):
            return decimal_capacitance_to_str(self.min) if self.min else ''

        def get_typ_display(self):
            return decimal_capacitance_to_str(self.typ) if self.typ else ''

        def get_max_display(self):
            return decimal_capacitance_to_str(self.max) if self.max else ''

        def get_condition_display(self):
            return "V<sub>CB</sub>={}, f={}, T<sub>A</sub>={}".format(
                decimal_voltage_to_str(self.at_collector_base_voltage),
                decimal_frequency_to_str(self.at_frequency),
                decimal_celsius_to_str(self.at_temp))


class TransistorBipolar(Part):
    part_type_subset = ['T', 'TBN', 'TBP']
    # absolute maximum ratings
    amr_at_temp = models.IntegerField(null=True, blank=True)
    collector_base_voltage = models.IntegerField(null=True, blank=True)
    collector_emitter_voltage = models.IntegerField(null=True, blank=True)
    emitter_base_voltage = models.IntegerField(null=True, blank=True)
    collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    peak_collector_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    peak_base_current = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    power_dissipation = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    operating_junction_temperature = models.IntegerField(null=True, blank=True)
    thermal_resistance_junction_case = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    # electrical characteristics
    collector_base_breakdown_voltage = BreakdownVoltage()  # BV_CBO
    collector_emitter_breakdown_voltage = BreakdownVoltage()  # BV_CEO
    emitter_base_breakdown_voltage = BreakdownVoltage()  # BV_EBO
    collector_emitter_cut_off_current1 = CECutOffCurrent()  # I_CES
    collector_emitter_cut_off_current2 = CECutOffCurrent()  # I_CES
    emitter_base_cut_off_current = BECutOffCurrent()  # I_EBO
    dc_current_gain1 = DCCurrentGain()  # h_FE
    dc_current_gain2 = DCCurrentGain()  # h_FE
    collector_emitter_saturation_voltage = CollectorEmitterSaturationVoltage()
    base_emitter_voltage = BaseEmitterVoltage()
    gain_bandwidth_product = GainBandwidthProduct()
    collector_base_capacitance = CollectorBaseCapacitance()

    def generate_description(self):
        return "{}, {}, {}".format(self.get_part_type_display(),
                                   decimal_current_to_str(self.collector_current),
                                   decimal_voltage_to_str(self.collector_emitter_voltage))

    def get_amr_at_temp_display(self):
        return decimal_celsius_to_str(self.amr_at_temp)

    def get_collector_base_voltage_display(self):
        return decimal_voltage_to_str(self.collector_base_voltage)

    def get_collector_emitter_voltage_display(self):
        return decimal_voltage_to_str(self.collector_emitter_voltage)

    def get_emitter_base_voltage_display(self):
        return decimal_voltage_to_str(self.emitter_base_voltage)

    def get_collector_current_display(self):
        return decimal_current_to_str(self.collector_current)

    def get_peak_collector_current_display(self):
        return decimal_current_to_str(self.peak_collector_current)

    def get_peak_base_current_display(self):
        return decimal_current_to_str(self.peak_base_current)

    def get_power_dissipation_display(self):
        return decimal_power_to_str(self.power_dissipation) if self.power_dissipation else ''

    def __str__(self):
        return "{}, {}".format(self.manufacturer_part_number, self.description)


