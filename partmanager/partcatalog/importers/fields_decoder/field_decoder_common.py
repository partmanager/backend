from decimal import Decimal


def parameter_str_to_dict(parameter_str, value_decoder):
    if parameter_str:
        parameter_str = parameter_str.strip()
        if 'max.' in parameter_str:
            parameter_str = parameter_str.replace('max.', '')
            return {'min': None, 'typ': None, 'max': value_decoder(parameter_str)}
        elif 'min.' in parameter_str:
            parameter_str = parameter_str.replace('min.', '')
            return {'min': value_decoder(parameter_str), 'typ': None, 'max': None}
        elif '~' in parameter_str:
            values_str = parameter_str.split('~')
            return {'min': value_decoder(values_str[0]), 'typ': None, 'max': value_decoder(values_str[1])}
        elif '±' in parameter_str:
            try:
                value_str, tolerance_str = parameter_str.split('±')
                value_str = value_str.strip()
                tolerance_str = tolerance_str.strip()
                #print(parameter_str, "value:", value_str, "tolerance:", tolerance_str)
                if len(value_str) > 0:
                    value = value_decoder(value_str)
                    assert value is not None, f"value should be not None but it is {value}, decoded from {value_str}, parameter_str: {parameter_str}"
                    if '%' in tolerance_str:
                        min_max = percent_str_to_decimal(tolerance_str) / Decimal(100)
                        return {'min': value - value * min_max, 'typ': value, 'max': value + value * min_max, 'tolerance_type': 'relative', 'relative_tolerance': min_max}
                    elif 'ppm' in tolerance_str:
                        min_max = ppm_str_to_decimal(tolerance_str) / Decimal(1000000)
                        return {'min': value - value * min_max, 'typ': value, 'max': value + value * min_max,
                                'tolerance_type': 'relative', 'relative_tolerance': min_max}
                    else:
                            min_max = value_decoder(tolerance_str)
                            return {'min': value - min_max, 'typ': value, 'max': value + min_max, 'tolerance_type': 'absolute'}
            except:
                print(parameter_str)
                raise
            else:
                min_max = value_decoder(tolerance_str)
                return {'min': min_max * -1, 'typ': None, 'max': min_max}

        else:
            if '+' in parameter_str and '-' in parameter_str:
                value_tolerance = parameter_str.replace('  ', ' ').strip().split(' ')
                tolerance = value_tolerance[1].split('/')
                value = value_decoder(value_tolerance[0])
                if '%' in tolerance[0]:
                    min_max = percent_str_to_decimal(tolerance[0]) / Decimal(100)
                    tolerance0 = min_max * value
                else:
                    tolerance0 = value_decoder(tolerance[0])
                if '%' in tolerance[1]:
                    min_max = percent_str_to_decimal(tolerance[1]) / Decimal(100)
                    tolerance1 = min_max * value
                else:
                    tolerance1 = value_decoder(tolerance[1])
                #print(parameter_str, value, tolerance0, tolerance1)
                if tolerance0 > tolerance1:
                    return {'min': value + tolerance1,
                            'typ': value,
                            'max': value + tolerance0}
                else:
                    return {'min': value + tolerance0,
                            'typ': value,
                            'max': value + tolerance1}
            # elif ' ' in parameter_str:
            #     typ_and_tolerance = parameter_str.split(' ')
            #     typ_value = value_decoder(typ_and_tolerance[0])
            #     tolerance_value = value_decoder(typ_and_tolerance[1])
            #     if tolerance_value > 0:
            #         value_dict = {'min': None, 'typ': typ_value, 'max': typ_value + tolerance_value}
            #     else:
            #         value_dict = {'min': typ_value + tolerance_value, 'typ': typ_value, 'max': None}
            #     return value_dict
            elif '+' in parameter_str:
                try:
                    typ_and_max_str = parameter_str.split('+')
                    typ_value = value_decoder(typ_and_max_str[0].strip())
                    max_value = typ_value + value_decoder(typ_and_max_str[1].strip())
                    value_dict = {'min': None, 'typ': typ_value, 'max': max_value}
        #            print(value_dict)
                    return value_dict
                except TypeError as e:
                    print(parameter_str)
                    print(typ_and_max_str)
                    raise
            elif '-' in parameter_str:
                typ_and_max_str = parameter_str.split('-')
                typ_value = value_decoder(typ_and_max_str[0])
                min_value = typ_value - value_decoder(typ_and_max_str[1])
                value_dict = {'min': min_value, 'typ': typ_value, 'max': None}
    #            print(value_dict)
                return value_dict
            else:
                return {'min': None, 'typ': value_decoder(parameter_str), 'max': None}


def percent_str_to_decimal(percent_str):
    if '%' in percent_str:
        return Decimal(percent_str.replace('%', ''))


def ppm_str_to_decimal(percent_str):
    if 'ppm' in percent_str:
        return Decimal(percent_str.replace('ppm', ''))