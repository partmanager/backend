import decimal
from decimal import Decimal
from packages.models.packages import add_package
from ..models.fields import Dimension
from ..models.ChipResistorPackage import ChipResistorPackage
from ..models.ChipCapacitorPackage import ChipCapacitorPackage
from ..models.SOPackage import SOPackage

package_type_map = {
    "Chip Resistor": ChipResistorPackage,
    "Chip Capacitor": ChipCapacitorPackage,
    "SO": SOPackage,
    "SOIC": SOPackage,
}


def str_to_dimension_and_tolerance(dimension_str):
    try:
        if 'mm' in dimension_str:
            if '±' in dimension_str:
                dimension_tolerance_str = dimension_str.replace('mm', '').split('±')
                return {'value': Decimal(dimension_tolerance_str[0]),
                        'tolerance_oversize': Decimal(dimension_tolerance_str[1]),
                        'tolerance_undersize': Decimal(dimension_tolerance_str[1]) * -1}
            elif '~' in dimension_str:
                dimension_tolerance_str = dimension_str.replace('mm', '').split('~')
                min = Decimal(dimension_tolerance_str[0])
                max = Decimal(dimension_tolerance_str[1])
                value = min + ((max - min) / 2)
                return {'value': value,
                        'tolerance_oversize': max - value,
                        'tolerance_undersize': min - value}
            elif 'min' in dimension_str:
                dimension_tolerance_str = dimension_str.replace('mm', '').replace('min.', '')
                min = Decimal(dimension_tolerance_str)
                max = None
                value = min
                return {'value': value,
                        'tolerance_oversize': None,
                        'tolerance_undersize': min - value}
            elif 'max' in dimension_str:
                dimension_tolerance_str = dimension_str.replace('mm', '').replace('max.', '')
                min = None
                max = Decimal(dimension_tolerance_str)
                value = max
                return {'value': value,
                        'tolerance_oversize': 0,
                        'tolerance_undersize': None}
            else:
                dimensions = dimension_str.replace('mm', '').split(' ')
                if len(dimensions) == 1:
                    return {'value': Decimal(dimensions[0]),
                            'tolerance_oversize': None,
                            'tolerance_undersize': None}
                else:
                    tolerance = dimensions[1].split('/')
                    return {'value': Decimal(dimensions[0]),
                            'tolerance_oversize': Decimal(tolerance[0].replace('+', '')),
                            'tolerance_undersize': Decimal(tolerance[1])}
    except decimal.InvalidOperation:
        print(dimension_str)
        raise


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


def part_dict_to_package(package_type, part_dictionary):
    if package_type in ['Chip Capacitor', 'Chip Inductor']:
        length = str_to_dimension_and_tolerance(part_dictionary['Length'])
        width = str_to_dimension_and_tolerance(part_dictionary['Width'])
        thickness_field_name = 'Thickness' if 'Thickness' in part_dictionary else 'Height'
        thickness = str_to_dimension_and_tolerance(part_dictionary[thickness_field_name])
        e = str_to_dimension_and_tolerance(part_dictionary['e'])
        g = str_to_dimension_and_tolerance(part_dictionary['g'])
        if g is None:
            g = {}
            g['value'] = length['value'] - 2*e['value']
            g['tolerance_pos'] = None
            g['tolerance_neg'] = None
        dimensions = {'length_value': length['value'],
                      'length_tolerance_oversize': length['tolerance_pos'],
                      'length_tolerance_undersize': length['tolerance_neg'],
                      'width_value': width['value'],
                      'width_tolerance_oversize': width['tolerance_pos'],
                      'width_tolerance_undersize': width['tolerance_neg'],
                      'thickness_value': thickness['value'],
                      'thickness_tolerance_oversize': thickness['tolerance_pos'],
                      'thickness_tolerance_undersize': thickness['tolerance_neg'],
                      'e_value': e['value'],
                      'e_tolerance_oversize': e['tolerance_pos'],
                      'e_tolerance_undersize': e['tolerance_neg'],
                      'g_value': g['value'],
                      'g_tolerance_oversize': g['tolerance_pos'],
                      'g_tolerance_undersize': g['tolerance_neg']
                      }
        name = package_dimensions_to_name(dimensions)
        return add_package(package_type, name, dimensions)
    elif package_type in ['Chip Resistor']:
        length = str_to_dimension_and_tolerance(part_dictionary['Length'])
        width = str_to_dimension_and_tolerance(part_dictionary['Width'])
        thickness_field_name = 'Thickness' if 'Thickness' in part_dictionary else 'Height'
        thickness = str_to_dimension_and_tolerance(part_dictionary[thickness_field_name])
        t1 = str_to_dimension_and_tolerance(part_dictionary['t1'])
        t2 = str_to_dimension_and_tolerance(part_dictionary['t2'])
        dimensions = {'length_value': length['value'],
                      'length_tolerance_oversize': length['tolerance_pos'],
                      'length_tolerance_undersize': length['tolerance_neg'],
                      'width_value': width['value'],
                      'width_tolerance_oversize': width['tolerance_pos'],
                      'width_tolerance_undersize': width['tolerance_neg'],
                      'thickness_value': thickness['value'],
                      'thickness_tolerance_oversize': thickness['tolerance_pos'],
                      'thickness_tolerance_undersize': thickness['tolerance_neg'],
                      't1_value': t1['value'],
                      't1_tolerance_oversize': t1['tolerance_pos'],
                      't1_tolerance_undersize': t1['tolerance_neg'],
                      't2_value': t2['value'],
                      't2_tolerance_oversize': t2['tolerance_pos'],
                      't2_tolerance_undersize': t2['tolerance_neg']
                      }
        name = part_dictionary['Package Type'].replace('Chip ', '')
        return add_package(package_type, name, dimensions)



def get_or_create_package_from_dict(package_dictionary):
    if 'package_type' in package_dictionary and 'dimensions' in package_dictionary:
        package_type = package_dictionary["package_type"]
        if package_type not in package_type_map:
            print("Unable to find package type", package_type)
            raise ValueError("Unsupported package type")
        else:
            dimensions = decode_dimensions(package_dictionary["dimensions"])
            print(dimensions)
            package_class = package_type_map[package_type]

            package_object, created = package_class.objects.get_or_create(
                type=package_type,
                name=package_dictionary["name"],
                description=package_class(package_dictionary["name"], dimensions),
                pin_count = package_dictionary["pin_count"],
                **dimensions)
            print(package_object, created)
            return package_object, created
    return None, False


def decode_dimensions(dimensions):
    decoded_dimensions = {}
    for key, value in dimensions.items():
        print(key, value)
        for k, v in str_to_dimension_and_tolerance(value).items():
            decoded_dimensions[f"{key}_{k}"] = v
    return decoded_dimensions