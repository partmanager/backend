import os
import decimal
import json
import logging
from enum import Enum
from urllib.parse import urlparse

from django.db import IntegrityError

from manufacturers.models import get_or_create_manufacturer_by_name
from packages.importers.package_importer import get_or_create_package_from_dict
from packages.models.common import Package
from partcatalog.models.part import Part
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.models.packaging import Packaging
from partcatalog.models.files import FileVersion, File
from symbolandfootprint.models import Symbol
from .common import  str_to_production_status
from .fields_decoder.storage_conditions_decoder import storage_conditions_decoder
from .fields_decoder.operating_conditions_decoder import operating_conditions_decoder

from part_library_gen import symbol_generator


logger = logging.getLogger('partcatalog')


class GenerateDescriptionPolicy(Enum):
    AlwaysGenerateDescription = 1
    GenerateDescriptionIfMissing = 2
    AlwaysUseFileDescription = 3


class ModelImporter:
    def __init__(self, model_class, part_type, generate_description):
        self.model_class = model_class
        self.part_type = part_type
        self.generate_description = generate_description
        self.parameters_todo = {'Working Temp Range'}

    def get_part(self, manufacturer, part_number):
        try:
            return self.model_class.objects.get(manufacturer=manufacturer, manufacturer_part_number=part_number)
        except self.model_class.DoesNotExist as e:
            return None
        # if len(part) == 1:
        #     return part[0]
        # elif len(part) > 1:
        #     logger.error("********************************** Multiple parts found")

    def create_part(self, manufacturer, part_number, json_data):
        logger.info(f"Creating {part_number}")
        package = self.get_or_create_package(json_data['package'])
        common_parameters = self.decode_common_part_parameters(json_data)
        #logger.debug(f"Decoded common part parameters: {common_parameters}")
        parameters = self.decode_parameters(json_data['parameters'])
        #logger.debug(f"Decoded part specific parameters: {parameters}")
        #     symbol = self.decode_symbol_and_footprint(json_data)
        #logger.debug(f"Decoded symbol and footprint: {symbol}")
        try:
            part = self.model_class(manufacturer_part_number=part_number,
                                    manufacturer=manufacturer,
                                    operating_conditions=self.decode_operating_conditions(json_data),
                                    storage_conditions=self.decode_storage_conditions(json_data['storageConditions']),
                                    **common_parameters,
                                    package=package,
                                    **parameters)  #,
        #                                symbol=symbol)
        except AttributeError as e:
            logger.error(f"{repr(e)}, {json_data}")
            return None
        if self.generate_description == GenerateDescriptionPolicy.AlwaysGenerateDescription:
            part.description = part.generate_description()
            logger.info(f"Generated description {part.description}")
        elif self.generate_description == GenerateDescriptionPolicy.GenerateDescriptionIfMissing:
            if 'description' in json_data and len(json_data['description']) > 0:
                part.description = json_data['description'] if 'description' in json_data else None
            else:
                part.description = part.generate_description()
                logger.info(f"Generated description {part.description}")
        elif self.generate_description == GenerateDescriptionPolicy.AlwaysUseFileDescription:
            part.description = json_data['description'] if 'description' in json_data else None
        logger.info(f"Created {part_number}, Package: {package}")
        return part

    def decode_storage_conditions(self, json_data):
        return storage_conditions_decoder(json_data)

    def decode_operating_conditions(self, json_data):
        return operating_conditions_decoder(
            json_data['operatingConditions'] if 'operatingConditions' in json_data else {})

    def decode_common_part_parameters(self, json_data):
        common_parameters = {
            'part_type': Part.part_type_from_str(json_data['partType'])
        }
        if 'production_status' in json_data:
            common_parameters['production_status'] = str_to_production_status(json_data['productionStatus'])
        if 'markingCode' in json_data and json_data['markingCode'] is not None and len(json_data['markingCode']):
            common_parameters['device_marking_code'] = json_data['markingCode']
        if 'series' in json_data and 'name' in json_data['series']:
            common_parameters['series'] = json_data['series']['name']
            common_parameters['series_description'] = json_data['series']['description'] if 'description' in json_data[
                'series'] else None
        if 'productUrl' in json_data and json_data['productUrl'] is not None and len(json_data['productUrl']):
            common_parameters['product_url'] = json_data['productUrl']
        if 'notes' in json_data and json_data['notes'] is not None and len(json_data['notes']):
            common_parameters['notes'] = json_data['notes']
        return common_parameters

    # def decode_symbol_and_footprint(self, json_data):
    #     if 'symbol&footprint' in json_data:
    #         symbol_footprint = json_data['symbol&footprint']
    #         if 'symbolName' in symbol_footprint:
    #             symbol_name = symbol_footprint['symbolName']
    #             return get_or_create_symbol(symbol_name)

    def get_or_create_package(self, package_data_json):
        try:
            package, created = get_or_create_package_from_dict(package_data_json)
            if created:
                logger.info(f"Created package {package.name}")
            return package
        except ValueError as e:
            logger.error(f"Exception during package generation {e}")
            return None

    def validate_parameters(self, json_data):
        json_parameters_set = set(json_data.keys())
        assert len(json_parameters_set) == len(json_data.keys())
        part_parameters_set = set(self.parameters_todo)
        for parameter in self.parameters:
            part_parameters_set.add(self.parameters[parameter]['json_field'])
        assert len(part_parameters_set) == len(self.parameters) + len(self.parameters_todo)

        if len(json_parameters_set.union(part_parameters_set)) > len(part_parameters_set):
            additional_parameters = str(json_parameters_set - part_parameters_set)
            logger.error(f"----------------> Error, additional parameters: {additional_parameters}")
            assert False, "Part have additional parameters that can't be parsed" + additional_parameters

    def decode_parameters(self, json_data):
        self.validate_parameters(json_data)
        decoded = {}
        for parameter in self.parameters:
            try:
                #logger.debug(f"Decoding parameter {parameter}")
                parameter_decoder = self.parameters[parameter]['decoder']
                json_field = self.parameters[parameter]['json_field']
                max_values_count = self.parameters[parameter]['max_values_count'] if 'max_values_count' in \
                                                                                     self.parameters[
                                                                                         parameter] else None
                if json_field in json_data:
                    if max_values_count:
                        if isinstance(json_data[json_field], list):
                            for index in range(min(max_values_count, len(json_data[json_field]))):
                                decoded_param = parameter_decoder(json_data[json_field][index])
                                if decoded_param:
                                    decoded['{}_{}'.format(parameter, index + 1)] = decoded_param
                        else:
                            decoded_param = parameter_decoder(json_data[json_field])
                            if decoded_param:
                                decoded['{}_1'.format(parameter)] = parameter_decoder(json_data[json_field])
                    else:
                        if isinstance(json_data[json_field], list):
                            logger.error("*********** Error, parameter is list but part model can't support it")
                            decoded[parameter] = parameter_decoder(json_data[json_field][0])
                        else:
                            try:
                                decoded[parameter] = parameter_decoder(json_data[json_field])
                            except KeyError as e:
                                logger.error(f"Key Error in {parameter} parameter parsing: {e}")
            except decimal.InvalidOperation as exception:
                logger.error(f"Decimal invalid operation exception {parameter}, {exception}")
        return decoded


class JsonImporterBase:
    def __init__(self):
        self.last_manufacturer = None
        self.parts = []
        self.dry_run = False
        self.skip_file_download = True
        self.part_decoders = {}
        self.logger = logging.getLogger('partcatalog')
        self.force_update = False

    def register_model_importer(self, model_importer):
        for part_type in model_importer.part_type:
            assert part_type not in self.part_decoders, "Part Importer already registered"
            self.part_decoders[part_type] = model_importer

    def parts_import(self, filename):
        self.logger.info("Importing parts from json file")
        with open(filename) as jsonfile:
            self.parts = json.load(jsonfile)

    def run(self, dry=False):
        self.dry_run = dry
        if self.parts:
            for part in self.parts:
                self.add_part(part)

    def add_part(self, json_data):
        manufacturer = self.get_manufacturer(json_data['manufacturer'])
        if manufacturer:
            part_type = json_data['partType']
            part_number = json_data['partNumber']
            part_importer = self.part_decoders[part_type]
            part = part_importer.get_part(manufacturer, part_number)
            imported_part = part_importer.create_part(manufacturer, part_number, json_data)
            if not part:
                if imported_part:
                    part = imported_part
                    self.__save(imported_part)
                    self.logger.info(f"{part.manufacturer_part_number} added")
            else:
                self.update_part(part, imported_part, part_importer)
                self.logger.info(f"{part.manufacturer_part_number} updated")

            self.add_manufacturer_order_numbers(manufacturer, part, json_data['orderNumbers'])
            if 'files' in json_data:
                self.add_files(part, json_data['files'])
            if "symbol&footprint" in json_data:
                symbol_footprint = json_data["symbol&footprint"]
                if "pinmap" in symbol_footprint and symbol_footprint["pinmap"]:
                    self.add_symbols(part, symbol_footprint)
        else:
            self.logger.error("Unknown manufacturer")

    def update_part(self, present, new, part_importer):
        updated = False
        for variable in vars(present):
            if variable not in ['_state', 'id', 'description']:
                present_value = getattr(present, variable)
                new_value = getattr(new, variable)
                if present_value != new_value and new_value is not None:
                    if present_value is None or (
                            isinstance(present_value, str) and len(present_value) == 0) or self.force_update:
                        updated = True
                        self.logger.debug(f"{variable}, present: {present_value}, New: {new_value}")
                        setattr(present, variable, new_value)
                    else:
                        self.logger.error(
                            f"============= Update Error. Unable to update: {variable}. Value conflict detected.")
                        self.logger.error(f"\tPresent value:\t, {present_value}, \n\tNew value:\t, {new_value}")
                        return
        if updated:
            if part_importer.generate_description == GenerateDescriptionPolicy.AlwaysGenerateDescription:
                present.generate_description()
            self.logger.info(f"************************** Saving updated part: {present}")
            present.save()

    def add_manufacturer_order_numbers(self, manufacturer, part, order_numbers):
        for order_number in order_numbers:
            packaging = self.decode_packaging(order_numbers[order_number])
            self.logger.debug(f'Updating MON: {order_number} for part {part.manufacturer_part_number}')
            if not self.dry_run:
                ManufacturerOrderNumber.objects.update_or_create(manufacturer_order_number=order_number,
                                                                 manufacturer=manufacturer,
                                                                 defaults={"packaging": packaging,
                                                                           "part": part})

    def decode_packaging(self, packaging_json):
        packaging = Packaging()
        packaging.code = None
        packaging.type = 'u'
        packaging.quantity = None
        packaging.packaging_data = None
        if packaging_json:
            packaging.code = packaging_json['Code'] if 'Code' in packaging_json else None
            packaging.type = packaging_json['Type'] if 'Type' in packaging_json else 'u'
            packaging.quantity = packaging_json['Qty'] if 'Qty' in packaging_json else None
            if packaging.type in ["Paper Tape / Reel", "Embossed Tape / Reel"] and 'PackagingData' in packaging_json:
                packaging.packaging_data = self.decode_tape_reel_packaging(packaging_json)
        return packaging

    def decode_tape_reel_packaging(self, packaging_json):
        return packaging_json['PackagingData'] if packaging_json['PackagingData'] else None

    def add_files(self, part, files_json):
        def get_filetype(field):
            if 'datasheet' in field:
                return 'd'
            if 'SPICEmodel' in field:
                return 'm'
            if 'Sparameter' in field:
                return 'p'
            else:
                return 'u'

        def get_or_create_file(file_data):
            parsed_url = urlparse(file_data['url'])
            filename = os.path.basename(parsed_url.path)
            defaults = {"name": filename,
                        "file_type": get_filetype(file_data),
                        "description": file_data['description'] if 'description' in file_data else None,
                        "manufacturer": part.manufacturer}
            obj, created = File.objects.update_or_create(url=file_data['url'],
                                                         defaults=defaults)
            if created:
                self.logger.info(f"File {filename} created")
            return obj

        files = []
        for file_type_str in files_json:
            file_dict = files_json[file_type_str]
            parsed_file = get_or_create_file(file_dict)
            if parsed_file not in part.files.all():
                part.files.add(parsed_file)
                self.__save(part)

            for file_version in file_dict['versions']:
                file_version_dict = file_dict['versions'][file_version]
                if 'md5sum' not in file_version_dict:
                    logger.error(f"Missing required 'md5sum' key for {file_type_str}, version: {file_version}")
                else:
                    update_data = {
                        'file_container': parsed_file,
                        'version': file_version,
                        'publication_date': file_version_dict['date'],
                        'url': file_version_dict['url'] if 'url' in file_version_dict else None,
                    }
                    file_version, created = FileVersion.objects.update_or_create(md5sum=file_version_dict['md5sum'],
                                                                                 defaults=update_data)
                    if created:
                        self.logger.info(f"File {file_version} created")
                    file_version_name = file_version.generate_filename(parsed_file.name)
                    if not file_version.file.name:
                        file_version.file.name = file_version_name
                        file_version.save()
                        self.logger.info(f"Assigned existing file into {file_version}")
        return files

    def add_symbols(self, part, symbol_footprint):
        #print(f"adding symbols, {symbol_footprint['pinmap']}")
        symbol_data = {
            'designator': "*",
            'manufacturer': "*",
            'part': "*",
            'pins': symbol_footprint['pinmap'],
            'symbol_generator': None
        }
        if 'symbol_generator' not in symbol_footprint:
            symbol_footprint['symbol_generator'] = {'default': {}}

        for generator in symbol_footprint['symbol_generator']:
            symbol_generator_data = symbol_footprint['symbol_generator'][generator]
            symbol_data['symbol_generator'] = {generator: symbol_footprint['symbol_generator'][generator]}
            generated = symbol_generator.generate(symbol_data)
            if generated:
                generated_symbol, symbol_name = generated[0]
                symbol_name = symbol_name.replace('*_*', '').replace('#', '')
                try:
                    symbol, created = Symbol.objects.update_or_create(symbol=generated_symbol.to_dict(),
                                                                      defaults={"name": symbol_name,
                                                                                "generator_name": generator,
                                                                                "generator_data": symbol_generator_data,
                                                                                "pinmap": symbol_footprint['pinmap']})
                    if created:
                        self.logger.info(f"Symbol for {part.manufacturer_part_number} created")
                    part.symbol = symbol
                    part.save()
                except IntegrityError as e:
                    print(e)

    def get_manufacturer(self, manufacturer_name):
        if self.last_manufacturer:
            if self.last_manufacturer.name == manufacturer_name:
                return self.last_manufacturer
        self.last_manufacturer = get_or_create_manufacturer_by_name(manufacturer_name)
        return self.last_manufacturer

    def __save(self, object_to_save):
        if not self.dry_run:
            object_to_save.save()
