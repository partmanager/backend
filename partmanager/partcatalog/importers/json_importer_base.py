import decimal
import json
import logging
import requests
from manufacturers.models import get_or_create_manufacturer_by_name
from .common import decode_common_part_parameters, decode_files, add_manufacturer_order_number, str_to_production_status
from .parameter_decoder import celsius_str_to_decimal, voltage_str_to_decimal
from partcatalog.models.part import Part
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.models.files import FileVersion, File, create_file_version_from_url
from symbolandfootprint.models import get_or_create_symbol
from .fields_decoder.storage_conditions_decoder import storage_conditions_decoder
from urllib.parse import urlparse
from enum import Enum
import os

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
        package = self.get_package(json_data['package'])
        parameters = self.decode_parameters(json_data['parameters'])
        common_parameters = self.decode_common_part_parameters(json_data)
        symbol = self.decode_symbol_and_footprint(json_data)
        part = self.model_class(manufacturer_part_number=part_number,
                                manufacturer=manufacturer,
                                storage_conditions=self.decode_storage_conditions(json_data['storageConditions']),
                                **common_parameters,
                                package=package,
                                **parameters,
                                symbol=symbol)
        if self.generate_description == GenerateDescriptionPolicy.AlwaysGenerateDescription:
            part.description = part.generate_description()
        elif self.generate_description == GenerateDescriptionPolicy.GenerateDescriptionIfMissing:
            if 'description' in json_data and len(json_data['description']) > 0:
                part.description = json_data['description']
            else:
                part.description = part.generate_description()
        elif self.generate_description == GenerateDescriptionPolicy.AlwaysUseFileDescription:
            part.description = json_data['description']
        return part

    def decode_storage_conditions(self, json_data):
        return storage_conditions_decoder(json_data)

    def decode_common_part_parameters(self, json_data):
        common_parameters = {
            'part_type': Part.part_type_from_str(json_data['partType'])
        }
        if 'production_status' in json_data:
            common_parameters['production_status'] = str_to_production_status(json_data['productionStatus'])
        if 'markingCode' in json_data and json_data['markingCode'] is not None and len(json_data['markingCode']):
            common_parameters['device_marking_code'] = json_data['markingCode']
        if 'series' in json_data:
            common_parameters['series'] = json_data['series']['name']
            common_parameters['series_description'] = json_data['series']['description']
        if 'productUrl' in json_data and json_data['productUrl'] is not None and len(json_data['productUrl']):
            common_parameters['product_url'] = json_data['productUrl']
        if 'notes' in json_data and json_data['notes'] is not None and len(json_data['notes']):
            common_parameters['notes'] = json_data['notes']
        return common_parameters

    def decode_symbol_and_footprint(self, json_data):
        if 'symbol&footprint' in json_data:
            symbol_footprint = json_data['symbol&footprint']
            symbol_name = symbol_footprint['symbolName']
            return get_or_create_symbol(symbol_name)

    def get_package(self, package_json):
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
                parameter_decoder = self.parameters[parameter]['decoder']
                json_field = self.parameters[parameter]['json_field']
                max_values_count = self.parameters[parameter]['max_values_count'] if 'max_values_count' in self.parameters[parameter] else None
                if json_field in json_data:
                    if max_values_count:
                        if isinstance(json_data[json_field], list):
                            for index in range(min(max_values_count, len(json_data[json_field]))):
                                decoded['{}_{}'.format(parameter, index + 1)] = parameter_decoder(json_data[json_field][index])
                        else:
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
                    if 'files' in json_data:
                        file = self.add_files(json_data['files'])
                        for f in file:
                            part.files.add(f)
                        self.__save(part)
                    self.logger.debug('%s %s', part.manufacturer_part_number, "\tAdd")
            else:
                self.update_part(part, imported_part, part_importer)
                self.logger.debug('%s %s', part.manufacturer_part_number, "\tSkip")

            self.add_manufacturer_order_numbers(manufacturer, part, json_data['orderNumbers'])
        else:
            self.logger.error("Unknown manufacturer")

    def update_part(self, present, new, part_importer):
        updated = False
        for variable in vars(present):
            if variable not in ['_state', 'id', 'description']:
                present_value = getattr(present, variable)
                new_value = getattr(new, variable)
                if present_value != new_value and new_value is not None:
                    if present_value is None or (isinstance(present_value, str) and len(present_value) == 0) or self.force_update:
                        updated = True
                        self.logger.debug(f"{variable}, present: {present_value}, New: {new_value}")
                        setattr(present, variable, new_value)
                    else:
                        self.logger.error(f"============= Update Error. Unable to update: {variable}. Value conflict detected.")
                        self.logger.error(f"\tPresent value:\t, {present_value}, \n\tNew value:\t, {new_value}")
                        return
        if updated:
            if part_importer.generate_description == GenerateDescriptionPolicy.AlwaysGenerateDescription:
                present.generate_description()
            self.logger.info(f"************************** Saving updated part: {present}")
            present.save()


    # def create_part(self, manufacturer, part_number, json_data):
    #     model_importer = self.model_decoders[json_data['partType']]
    #     if model_importer:
    #         package = self.get_package(json_data['package'])
    #         parameters = json_data['parameters']
    #         common_parameters = self.decode_common_part_parameters(json_data)
    #         part = model_importer.model_class(manufacturer_part_number=part_number,
    #                                           manufacturer=manufacturer,
    #                                           **common_parameters,
    #                                           package=package)
    #         if model_importer.generate_description:
    #             part.description = part.generate_description()
    #         else:
    #             part.description = json_data['description']
    #         return part

    def add_manufacturer_order_numbers(self, manufacturer, part, order_numbers):
        for order_number in order_numbers:
            mon = ManufacturerOrderNumber.objects.filter(manufacturer_order_number=order_number,
                                                         manufacturer=manufacturer)
            packaging = self.decode_packaging(order_numbers[order_number])
            if len(mon) == 0:
                self.logger.debug('%s %s', 'Adding MON for part', part.manufacturer_part_number)
                order_number = ManufacturerOrderNumber(manufacturer_order_number=order_number,
                                                       manufacturer=manufacturer,
                                                       **packaging,
                                                       part=part)
                # print(order_number.packaging.to_dict())
                self.__save(order_number)
            elif not self.dry_run:
                ManufacturerOrderNumber.objects.update_or_create(manufacturer_order_number=order_number,
                                                                 manufacturer=manufacturer,
                                                                 #part=part,
                                                                 defaults=packaging)

    def decode_packaging(self, packaging_json):
        if packaging_json:
            if packaging_json['Packaging Type'] in ["Paper Tape / Reel", "Embossed Tape / Reel"]:
                return self.decode_tape_reel_packaging(packaging_json)
        return {}

    def decode_tape_reel_packaging(self, packaging_json):
        return {}

    def add_files(self, files_json):
        def get_filetype(field):
            if 'datasheet' in field:
                return 'd'
            if 'SPICEmodel' in field:
                return 'm'
            if 'Sparameter' in field:
                return 'p'
            else:
                return 'u'

        files = []
        for file in files_json:
            filetype = get_filetype(file)
            url = files_json[file]
            found = File.objects.filter(url=url)
            if found:
                files.append(found[0])
            else:
                # file not exist, lets create one
                self.logger.debug(f"Adding file: {files_json[file]}")
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                #print(filename)
                file = File(url=url, name=filename, file_type=filetype)
                self.__save(file)
                if not self.skip_file_download:
                    try:
                        create_file_version_from_url(file_model=file, filename=filename, version='unknown', url=url)
                    except requests.exceptions.ReadTimeout:
                        self.logger.error('File download timeout, %s', url)
                # file_version = FileVersion(file=url, file_container=file, version='')
                # file_version.save()
                files.append(file)
        self.logger.info(f"Added {len(files)}, files")
        return files

    def get_manufacturer(self, manufacturer_name):
        if self.last_manufacturer:
            if self.last_manufacturer.name == manufacturer_name:
                return self.last_manufacturer
        self.last_manufacturer = get_or_create_manufacturer_by_name(manufacturer_name)
        return self.last_manufacturer

    def __save(self, object_to_save):
        if not self.dry_run:
            object_to_save.save()
