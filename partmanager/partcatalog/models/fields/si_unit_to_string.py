import decimal


def decimal_current_to_str(current):
    if current >= 1:
        return str(current).rstrip('0').rstrip('.') + 'A'
    elif current >= decimal.Decimal('0.001'):
        return str(current * 1000).rstrip('0').rstrip('.') + 'mA'
    elif current >= decimal.Decimal('0.000001'):
        return str(current * 1000000).rstrip('0').rstrip('.') + 'uA'
    elif current >= decimal.Decimal('0.000000001'):
        return str(current * 1000000000).rstrip('0').rstrip('.') + 'nA'


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


def decimal_resistance_to_str(frequency):
    if frequency >= 1000000:
        return str(frequency / 1000000).rstrip('0').rstrip('.') + 'M\u2126'
    elif frequency >= 1000:
        return str(frequency / 1000).rstrip('0').rstrip('.') + 'k\u2126'
    elif frequency >= 1:
        value_str = str(frequency)
        if '.' in value_str:
            value_str = value_str.rstrip('0').rstrip('.')
        return value_str + '\u2126'
    elif frequency >= decimal.Decimal('0.001'):
        return str(frequency * 1000).rstrip('0').rstrip('.') + 'm\u2126'
    elif frequency >= decimal.Decimal('0.000001'):
        return str(frequency * 1000000).rstrip('0').rstrip('.') + 'u\u2126'


def decimal_impedance_to_str(impedance):
    return decimal_resistance_to_str(impedance)


def decimal_inductance_to_str(inductance):
    if inductance >= 1000000:
        return str(inductance / 1000000).rstrip('0').rstrip('.') + 'MH'
    elif inductance >= 1000:
        return str(inductance / 1000).rstrip('0').rstrip('.') + 'kH'
    elif inductance >= 1:
        return str(inductance).rstrip('0').rstrip('.') + 'H'
    elif inductance >= decimal.Decimal('0.001'):
        return str(inductance * 1000).rstrip('0').rstrip('.') + 'mH'
    elif inductance >= decimal.Decimal('0.000001'):
        return str(inductance * 1000000).rstrip('0').rstrip('.') + 'uH'
    else:# inductance >= decimal.Decimal('0.000000001'):
        return str(inductance * 1000000000).rstrip('0').rstrip('.') + 'nH'

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
