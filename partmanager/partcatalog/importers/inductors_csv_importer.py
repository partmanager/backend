import decimal

from partcatalog.models.inductor import Inductor
from partcatalog.importers.package_importer import part_dict_to_package
from .common import decode_common_part_parameters
from .parameter_decoder import decode_current_parameter, decode_inductance_parameter, decode_parameter, decode_frequency_condition, \
    decode_frequency_parameter, decode_integer_parameter, decode_parameter_and_tolerance, celsius_str_to_decimal
from .units_decoder import decode_dc_resistance, decode_dc_saturation_current
from .csv_importer_base import CSVImporterBase


class InductorCSVImporter(CSVImporterBase):
    def __init__(self):
        super().__init__(Inductor)

    def create_part(self, manufacturer, part_number, dictionary):
        package = part_dict_to_package(dictionary['Package Type'], dictionary)
        common_parameters = decode_common_part_parameters(dictionary)

        inductance_and_tolerance = decode_inductance_and_tolerance(dictionary)
        dc_resistance = decode_dc_resistance(dictionary['DCR'], 'dc_resistance')
        dc_rated_current = decode_dc_rated_current(dictionary)
        q_factor = decode_q_factor(dictionary)
        dc_saturation_current = decode_dc_saturation_current(dictionary['DC Saturation Current'], 'dc_saturation_current')
        srf = decode_srf(dictionary)
        print(inductance_and_tolerance, dc_resistance, dc_rated_current, q_factor, dc_saturation_current, srf)
        part = Inductor(manufacturer_part_number=part_number,
                        manufacturer=manufacturer,
                        package=package,
                        **common_parameters,
                        # Inductor specific fields
                        **inductance_and_tolerance,
                        **dc_resistance,
                        **dc_rated_current,
                        **q_factor,
                        **dc_saturation_current,
                        **srf
                        )
        part.description = part.generate_description()
        return part


def decode_tolerance(tolerance_str):
    if '%' in tolerance_str:
        if '±' in tolerance_str:
            tolerance_str = tolerance_str.replace('±', '').replace('%', '')
            tolerance = decimal.Decimal(tolerance_str)
            return {'over': tolerance, 'under': tolerance * -1, 'type': '%'}
    else:
        tolerance = decode_inductance_parameter(tolerance_str)
        return {'over': tolerance['max'], 'under': tolerance['min'], 'type': 'H'}


def decode_inductance_and_tolerance(dictionary):
    if 'Inductance @ 100kHz, 0.25V' in dictionary:
        inductance_str = dictionary['Inductance @ 100kHz, 0.25V']
    else:
        inductance_str = dictionary['Inductance']
    inductance = decode_parameter_and_tolerance(inductance_str, decode_inductance_parameter,
                                                [decode_frequency_condition])
    if len(inductance) >= 1:
        inductance_typ = inductance[0]['value']
        tolerance = inductance[0]['tolerance']
        if inductance[0]['tolerance']['type'] == '%':
            return {'inductance_min': inductance_typ + inductance_typ * tolerance['under'] / 100,
                    'inductance_typ': inductance_typ,
                    'inductance_max': inductance_typ + inductance_typ * tolerance['over'] / 100,
                    'inductance_at_frequency': inductance[0]['at_frequency'],
                    'inductance_at_temp': decimal.Decimal('25'),
                    'inductance_tolerance_over': tolerance['over'],
                    'inductance_tolerance_under': tolerance['under'],
                    'inductance_tolerance_type': tolerance['type']}
        else:
            inductance_dict = {'inductance_min': inductance_typ + tolerance['under'],
                               'inductance_typ': inductance_typ,
                               'inductance_max': inductance_typ + tolerance['over'],
                               'inductance_at_frequency': inductance[0]['at_frequency'],
                               'inductance_at_temp': decimal.Decimal('25'),
                               'inductance_tolerance_over': tolerance['over'] * 1000000,
                               'inductance_tolerance_under': tolerance['under'] * 1000000,
                               'inductance_tolerance_type': 'uH'}
            print(inductance_dict)
            return inductance_dict


def decode_dc_rated_current(dictionary):
    for key in dictionary:
        if 'DC Rated Current' in key:
            dc_rated_current_str = dictionary[key]
            at_temperature = celsius_str_to_decimal(key.replace('DC Rated Current @', ''))
            if dc_rated_current_str:
                dc_rated_current = decode_current_parameter(dc_rated_current_str)
                dc_rated_current['at_temp'] = at_temperature
                return {'dc_rated_current_' + k: v for k, v in dc_rated_current.items()}
    return {}


def decode_q_factor(dictionary):
    q_str = dictionary['Q']
    if q_str:
        q = decode_parameter(q_str, decode_integer_parameter, [decode_frequency_condition])
        if q:
            return {'q_factor_' + k: v for k, v in q[0].items()}
        else:
            return {}
    return {}


def decode_srf(dictionary):
    srf_str = dictionary['SRF']
    if srf_str:
        srf = decode_frequency_parameter(srf_str)
        result = {'srf_' + k: v for k, v in srf.items()}
        print(result)
        return result
    else:
        return {}









