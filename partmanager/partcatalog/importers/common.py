import decimal
import os

from .parameter_decoder import decode_temperature_parameter, decode_parameter, decode_distance_parameter
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.models.part import Part
from partcatalog.models.files import FileVersion, File, create_file_version_from_url
from symbolandfootprint.models import get_symbol_by_name
from urllib.parse import urlparse


def decode_common_part_parameters(dictionary):
    working_temp_range = decode_temperature_parameter(dictionary['Working Temp Range'])
    storage_temp_range = decode_temperature_parameter(dictionary['Storage Temp Range'])
    common_parameters = {'part_type': Part.part_type_from_str(dictionary['Part Type']),
                         'series': dictionary['Series'],
                         'series_description': dictionary['Series Description'],
                         'production_status': str_to_production_status(dictionary['Production Status']),
                         'device_marking_code': dictionary['Marking Code'],
                         'notes': dictionary['Notes'],
                         'product_url': dictionary['Product URL'],
                         'working_temperature_min': working_temp_range['min'],
                         'working_temperature_max': working_temp_range['max'],
                         'storage_temperature_min': storage_temp_range['min'],
                         'storage_temperature_max': storage_temp_range['max'],
                         'symbol': get_symbol_by_name(dictionary['Symbol']) if 'Symbol' in dictionary else None
                         }
    return common_parameters


def decode_tape_reel_packaging(dictionary):
    def decode_distance(distance_str):
        if '"' in distance_str or '”' in distance_str:
            return decimal.Decimal(distance_str.replace('"', '').replace('”', ''))
        else:
            distance = decode_parameter(distance_str, decode_distance_parameter, [])
            if len(distance) == 1:
                return distance[0]['typ'] * 1000

    packaging = {'packaging_code': dictionary['Packaging Code'] if 'Packaging Code' in dictionary else None,
                 'packaging_type': dictionary['Packaging Type'] if 'Packaging Type' in dictionary else None,
                 'packaging_quantity': dictionary['Packaging Qty'] if dictionary['Packaging Qty'] else None}
    if dictionary['Packaging Type'] in ['Paper Tape / Reel', 'Embossed Tape / Reel']:
        tape_reel = {'packaging_reel_diameter': decode_distance(dictionary['Reel Diameter']),
                     'packaging_reel_diameter_unit': '',
                     'packaging_reel_width': decode_distance(dictionary['Reel Width']),
                     'packaging_tape_pin_1_quadrant': ManufacturerOrderNumber.quadrant_from_str(
                         dictionary['Tape Pin 1 Quadrant']),
                     'packaging_tape_w': decode_distance(dictionary['Tape W']),
                     'packaging_tape_t': decode_distance(dictionary['Tape T']),
                     'packaging_tape_k': decode_distance(dictionary['Tape K']),
                     'packaging_tape_e': decode_distance(dictionary['Tape E']),
                     'packaging_tape_f': decode_distance(dictionary['Tape F']),
                     'packaging_tape_d': decode_distance(dictionary['Tape D']),
                     'packaging_tape_d1': decode_distance(dictionary['Tape D1']),
                     'packaging_tape_p0': decode_distance(dictionary['Tape P0']),
                     'packaging_tape_p1': decode_distance(dictionary['Tape P1']),
                     'packaging_tape_p2': decode_distance(dictionary['Tape P2']),
                     'packaging_tape_a0': decode_distance(dictionary['Tape A0']),
                     'packaging_tape_a1': decode_distance(dictionary['Tape A1']),
                     'packaging_tape_b0': decode_distance(dictionary['Tape B0']),
                     'packaging_tape_b1': decode_distance(dictionary['Tape B1'])}
        packaging.update(tape_reel)
    return packaging


def decode_files(dictionary):
    def get_filetype(field):
        if 'Datasheet' in field:
            return 'd'
        if 'SPICE model' in field:
            return 'm'
        if 'S parameter' in field:
            return 'p'
        else:
            return 'u'

    files = []
    for field in dictionary:
        if 'File' in field:
            filetype = get_filetype(field)
            url = dictionary[field]
            found = File.objects.filter(url=url)
            if found:
                files.append(found[0])
            else:
                # file not exist, lets create one
                print("Adding file:", dictionary[field])
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                file = File(url=url, name=filename, file_type=filetype)
                file.save()
                create_file_version_from_url(file_model=file, filename=filename, version='unknown', url=url)
                # file_version = FileVersion(file=url, file_container=file, version='')
                # file_version.save()
                files.append(file)
    return files


def str_to_production_status(status_str):
    if status_str:
        if 'In Production' in status_str:
            return 'ACT'
        if 'NRND' in status_str:
            return 'NRD'
        if 'To be discontinued' in status_str:
            return 'LTB'
    return 'UNK'


def str_to_voltage(voltage_str):
    if 'V' in voltage_str:
        if '±' in voltage_str:
            voltage_and_tolerance = voltage_str.replace('V', '').split('±')
            voltage = decimal.Decimal(voltage_and_tolerance[0])
            tolerance = decimal.Decimal(voltage_and_tolerance[1])
            return [voltage, tolerance * -1, tolerance]
        else:
            voltage_and_tolerance = voltage_str.replace('V', '').split(' ')
            voltage = decimal.Decimal(voltage_and_tolerance[0])
            tolerance_str = voltage_and_tolerance[1].split('/')
            tolerance_a = decimal.Decimal(tolerance_str[0].replace('+', ''))
            tolerance_b = decimal.Decimal(tolerance_str[1].replace('+', ''))
            if tolerance_a > tolerance_b:
                return [voltage, tolerance_a, tolerance_b]
            else:
                return [voltage, tolerance_b, tolerance_a]


def add_manufacturer_order_number(manufacturer, part, dictionary):
    mon = ManufacturerOrderNumber.objects.all().filter(manufacturer_order_number=dictionary['Order Number'],
                                                       manufacturer=manufacturer)
    if len(mon) == 0:
        print('Adding MON for part', part.manufacturer_part_number)
        packaging = decode_tape_reel_packaging(dictionary)
        order_number = ManufacturerOrderNumber(manufacturer_order_number=dictionary['Order Number'],
                                               manufacturer=manufacturer,
                                               **packaging,
                                               part=part)
        order_number.save()
        return order_number
    # else:
        #packaging = decode_tape_reel_packaging(dictionary)
        #object, crated = ManufacturerOrderNumber.objects.update_or_create(
        #    manufacturer_order_number=dictionary['Order Number'],
        #    manufacturer=manufacturer,
        #    part=part,
        #    defaults=packaging)
        #print(crated)