import decimal
from decimal import Decimal


def decode_dimensions(dimensions):
    decoded_dimensions = {}
    for key, value in dimensions.items():
        for k, v in str_to_dimension_and_tolerance(value).items():
            decoded_dimensions[f"{key.lower()}_{k}"] = v
    return decoded_dimensions


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