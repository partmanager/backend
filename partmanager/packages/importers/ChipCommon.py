from decimal import Decimal


def package_dimensions_to_name(dimensions):
    if dimensions['length_value'] == Decimal('0.3') and dimensions['width_value'] == Decimal('0.15'):
        return '0075'
    if dimensions['length_value'] == Decimal('0.4') and dimensions['width_value'] == Decimal('0.2'):
        return '0100'
    if dimensions['length_value'] == Decimal('0.25') and dimensions['width_value'] == Decimal('0.125'):
        return '008004'
    if dimensions['length_value'] == Decimal('0.4') and dimensions['width_value'] == Decimal('0.2'):
        return '01005'
    if dimensions['length_value'] == Decimal('0.5') and dimensions['width_value'] == Decimal('0.25'):
        return '015008'
    if dimensions['length_value'] == Decimal('0.6') and dimensions['width_value'] == Decimal('0.3'):
        return '0201'
    if dimensions['length_value'] == Decimal('1.0') and dimensions['width_value'] == Decimal('0.5'):
        return '0402'
    if dimensions['length_value'] == Decimal('1.55') and dimensions['width_value'] == Decimal('0.80'):
        return '0603'
    if dimensions['length_value'] == Decimal('1.55') and dimensions['width_value'] == Decimal('0.85'):
        return '0603'
    if dimensions['length_value'] == Decimal('1.6') and dimensions['width_value'] == Decimal('0.8'):
        return '0603'
    if dimensions['length_value'] == Decimal('1.6') and dimensions['width_value'] == Decimal('0.81'):
        return '0603'
    if dimensions['length_value'] == Decimal('1.8') and dimensions['width_value'] == Decimal('1.0'):
        return '0704'
    if dimensions['length_value'] == Decimal('2.0') and dimensions['width_value'] == Decimal('1.2'):
        return '0805'
    if dimensions['length_value'] == Decimal('2.0') and dimensions['width_value'] == Decimal('1.25'):
        return '0805'
    if dimensions['length_value'] == Decimal('2.01') and dimensions['width_value'] == Decimal('1.25'):
        return '0805'
    if dimensions['length_value'] == Decimal('3.05') and dimensions['width_value'] == Decimal('1.55'):
        return '1206'
    if dimensions['length_value'] == Decimal('3.1') and dimensions['width_value'] == Decimal('1.55'):
        return '1206'
    if dimensions['length_value'] == Decimal('3.1') and dimensions['width_value'] == Decimal('1.6'):
        return '1206'
    if dimensions['length_value'] == Decimal('3.2') and dimensions['width_value'] == Decimal('1.6'):
        return '1206'
    if dimensions['length_value'] == Decimal('3.1') and dimensions['width_value'] == Decimal('2.4'):
        return '1210'
    if dimensions['length_value'] == Decimal('3.1') and dimensions['width_value'] == Decimal('2.6'):
        return '1210'
    if dimensions['length_value'] == Decimal('3.2') and dimensions['width_value'] == Decimal('2.5'):
        return '1210'
    if dimensions['length_value'] == Decimal('3.1') and dimensions['width_value'] == Decimal('4.6'):
        return '1218'
    if dimensions['length_value'] == Decimal('4.5') and dimensions['width_value'] == Decimal('2.0'):
        return '1808'
    if dimensions['length_value'] == Decimal('4.5') and dimensions['width_value'] == Decimal('3.2'):
        return '1812'
    if dimensions['length_value'] == Decimal('4.9') and dimensions['width_value'] == Decimal('2.4'):
        return '2010'
    if dimensions['length_value'] == Decimal('5.0') and dimensions['width_value'] == Decimal('2.5'):
        return '2010'
    if dimensions['length_value'] == Decimal('5.0') and dimensions['width_value'] == Decimal('5.0'):
        return '2020'
    if dimensions['length_value'] == Decimal('5.7') and dimensions['width_value'] == Decimal('5.0'):
        return '2220'
    if dimensions['length_value'] == Decimal('6.2') and dimensions['width_value'] == Decimal('3.2'):
        return '2412'
    if dimensions['length_value'] == Decimal('6.30') and dimensions['width_value'] == Decimal('3.10'):
        return '2512'
    if dimensions['length_value'] == Decimal('6.30') and dimensions['width_value'] == Decimal('3.15'):
        return '2512'
    if dimensions['length_value'] == Decimal('6.35') and dimensions['width_value'] == Decimal('3.1'):
        return '2512'
    if dimensions['length_value'] == Decimal('6.35') and dimensions['width_value'] == Decimal('3.2'):
        return '2512'
    if dimensions['length_value'] == Decimal('6.4') and dimensions['width_value'] == Decimal('3.2'):
        return '2512'
    if dimensions['length_value'] == Decimal('9.1') and dimensions['width_value'] == Decimal('9.4'):
        return '3637'
    raise ValueError("Unrecognized package dimensions", dimensions)
