import decimal


def decimal_celsius_to_str(celsius):
    if celsius:
        return str(celsius).rstrip('0').rstrip('.') + '℃'


def decimal_time_to_str(value):
    return str(value) + 's'


def decimal_ppm_to_str(value):
    if abs(value) >= 1:
        value_str = str(value)
        if '.' in value_str:
            value_str = value_str.rstrip('0').rstrip('.')
        return value_str + 'ppm'
    elif abs(value) >= decimal.Decimal('0.001'):
        return str(value * 1000).rstrip('0').rstrip('.') + 'ppm'
    elif abs(value) >= decimal.Decimal('0.000001'):
        return str(value * 1000000).rstrip('0').rstrip('.') + 'ppm'
    elif abs(value) >= decimal.Decimal('0.000000001'):
        return str(value * 1000000000).rstrip('0').rstrip('.') + 'ppm'


def decimal_capacitance_to_str(capacitance):
    if capacitance >= 1:
        return str(capacitance).rstrip('0').rstrip('.') + 'F'
    elif capacitance >= decimal.Decimal('0.001'):
        return str(capacitance * 1000).rstrip('0').rstrip('.') + 'mF'
    elif capacitance >= decimal.Decimal('0.000001'):
        return str(capacitance * 1000000).rstrip('0').rstrip('.') + 'uF'
    elif capacitance >= decimal.Decimal('0.000000001'):
        return str(capacitance * 1000000000).rstrip('0').rstrip('.') + 'nF'
    elif capacitance >= decimal.Decimal('0.000000000001'):
        return str(capacitance * 1000000000000).rstrip('0').rstrip('.') + 'pF'
    else:
        return str(capacitance * 1000000000000000).rstrip('0').rstrip('.') + 'fF'


def decimal_resistance_to_str(resistance_in_ohms):
    divider = {'m\u2126': decimal.Decimal('1e-3'), '\u2126': decimal.Decimal('1'),
               'k\u2126': decimal.Decimal('1e3'), 'M\u2126': decimal.Decimal('1e6')}
    for sufix in ['M\u2126', 'k\u2126', '\u2126', 'm\u2126']:
        if resistance_in_ohms >= divider[sufix]:
            return "{}".format(resistance_in_ohms / divider[sufix]).rstrip('0').rstrip('.') + sufix
    return "{}m\u2126".format(resistance_in_ohms / decimal.Decimal('1e-3'))


def decimal_decibel_to_str(decibel):
    return str(decibel) + 'dB'


def decimal_degree_to_str(degree):
    return str(degree) + '°'


def decimal_frequency_to_str(frequency):
    if frequency >= 1000000000:
        return str(frequency / 1000000000).rstrip('0').rstrip('.') + 'GHz'
    elif frequency >= 1000000:
        return str(frequency / 1000000).rstrip('0').rstrip('.') + 'MHz'
    elif frequency >= 1000:
        return str(frequency / 1000).rstrip('0').rstrip('.') + 'kHz'
    elif frequency >= 1:
        return str(frequency).rstrip('0').rstrip('.') + 'Hz'
    elif frequency >= decimal.Decimal('0.001'):
        return str(frequency * 1000).rstrip('0').rstrip('.') + 'mHz'
    elif frequency >= decimal.Decimal('0.000001'):
        return str(frequency * 1000000).rstrip('0').rstrip('.') + 'uHz'


def decimal_power_to_str(current):
    if current >= 1:
        return str(current).rstrip('0').rstrip('.') + 'W'
    elif current >= decimal.Decimal('0.001'):
        return str(current * 1000).rstrip('0').rstrip('.') + 'mW'
    elif current >= decimal.Decimal('0.000001'):
        return str(current * 1000000).rstrip('0').rstrip('.') + 'uW'
    elif current >= decimal.Decimal('0.000000001'):
        return str(current * 1000000000).rstrip('0').rstrip('.') + 'nW'


def decimal_rad_to_str(rad):
    return str(rad) + 'rad'


def decimal_voltage_to_str(voltage):
    if voltage == decimal.Decimal('0'):
        return '0V'
    elif voltage >= 1:
        voltage_str = str(voltage)
        if '.' in voltage_str:
            return voltage_str.rstrip('0').rstrip('.') + 'V'
        else:
            return voltage_str + 'V'
    elif voltage >= decimal.Decimal('0.001'):
        return str(voltage * 1000).rstrip('0').rstrip('.') + 'mV'
    elif voltage >= decimal.Decimal('0.000001'):
        return str(voltage * 1000000).rstrip('0').rstrip('.') + 'uV'