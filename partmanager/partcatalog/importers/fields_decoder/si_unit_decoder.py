from decimal import Decimal


def capacitance_decode(capacitance_str):
    return __si_capacitance_decoder.decode(capacitance_str)


def capacity_decode(capacity_str):
    return __si_capacity_decoder.decode(capacity_str)


def luminous_intensity_decode(luminous_intensity_str):
    return __si_luminous_intensity.decode(luminous_intensity_str)


def current_decode(current_str):
    return __si_current_decoder.decode(current_str)


def distance_decode(distance_str):
    return __si_distance_decoder.decode(distance_str)


def frequency_decode(freq_str):
    return __si_frequency_decoder.decode(freq_str)


def inductance_decode(inductance_str):
    return __si_inductance_decoder.decode(inductance_str)


def power_decode(power_str):
    return __si_power_decoder.decode(power_str)


def resistance_decode(resistance_str):
    return __si_resistance_decoder.decode(resistance_str)


def temperature_decode(time_str):
    return __si_temperature_decoder.decode(time_str)


def time_decode(time_str):
    return __si_time_decoder.decode(time_str)


def voltage_decode(voltage_str):
    return __si_voltage_decoder.decode(voltage_str)


class SiUnitDecoderBase:
    def __init__(self, unit):
        self.prefix = {'f': Decimal('0.000000000000001'),
                       'p': Decimal('0.000000000001'),
                       'n': Decimal('0.000000001'),
                       'u': Decimal('0.000001'),
                       'μ': Decimal('0.000001'),
                       'm': Decimal('0.001'),
                       'k': Decimal(1000),
                       'M': Decimal(1000000),
                       'G': Decimal(1000000000),
                       'T': Decimal(1000000000000),
                       '':  Decimal(1)}
        self.sufix_mul = {}
        self.__generate_sufix_dict(unit)

    def decode(self, value_str):
        for sufix in self.sufix_mul:
            if sufix in value_str:
                value_str = value_str.replace(sufix, '')
                try:
                    value = Decimal(value_str) * self.sufix_mul[sufix]
                    return value
                except:
                    print("SI unit decoder, Unable to convert", value_str)
                    raise

    def __generate_sufix_dict(self, unit):
        if isinstance(unit, list):
            for unit_symbol in unit:
                for prefix in self.prefix:
                    self.sufix_mul[prefix + unit_symbol] = self.prefix[prefix]
        else:
            for prefix in self.prefix:
                self.sufix_mul[prefix + unit] = self.prefix[prefix]


class SiTimeDecoder(SiUnitDecoderBase):
    def __init__(self):
        super().__init__('s')


class SiVoltageDecoder(SiUnitDecoderBase):
    def __init__(self):
        super().__init__('V')


__si_current_decoder = SiUnitDecoderBase('A')
__si_capacitance_decoder = SiUnitDecoderBase('F')
__si_capacity_decoder = SiUnitDecoderBase('Ah')
__si_luminous_intensity = SiUnitDecoderBase('cd')
__si_distance_decoder = SiUnitDecoderBase('m')
__si_frequency_decoder = SiUnitDecoderBase('Hz')
__si_inductance_decoder = SiUnitDecoderBase('H')
__si_power_decoder = SiUnitDecoderBase('W')
__si_resistance_decoder = SiUnitDecoderBase(['R', 'Ω', 'Ω'])
__si_temperature_decoder = SiUnitDecoderBase(['°C', '\u2103'])
__si_time_decoder = SiTimeDecoder()
__si_voltage_decoder = SiVoltageDecoder()

