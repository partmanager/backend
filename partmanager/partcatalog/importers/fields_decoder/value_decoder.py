from decimal import Decimal


def integer_decode(value_str):
    return Decimal(value_str)


def thermal_resistance(tr_str):
    if '°C/W' in tr_str:
        return Decimal(tr_str.replace('°C/W', ''))


def dB_decode(value_str):
    if 'dB' in value_str:
        return Decimal(value_str.replace('dB', ''))


def ppm_decode(value_str):
    if 'ppm' in value_str:
        return Decimal(value_str.replace('ppm', ''))


def ppm_per_year_decode(value_str):
    if 'ppm/year' in value_str:
        return Decimal(value_str.replace('ppm/year', ''))


def ppm_per_deg_decode(value_str):
    if 'ppm/°C' in value_str:
        return Decimal(value_str.replace('ppm/°C', ''))
    elif 'ppm/K' in value_str:
        return Decimal(value_str.replace('ppm/K', ''))
