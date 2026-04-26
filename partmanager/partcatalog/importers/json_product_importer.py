import decimal
import logging
from enum import Enum

from partcatalog.models.product import Product, ProductSeries, StorageConditions
from .fields_decoder.storage_conditions_decoder import storage_conditions_decoder
from .fields_decoder.operating_conditions_decoder import operating_conditions_decoder


logger = logging.getLogger('partcatalog')


class GenerateDescriptionPolicy(Enum):
    AlwaysGenerateDescription = 1
    GenerateDescriptionIfMissing = 2
    AlwaysUseFileDescription = 3


def decode_storage_conditions(json_data):
    if 'storageConditions' in json_data:
        return storage_conditions_decoder(json_data['storageConditions'])
    else:
        return storage_conditions_decoder({})


def decode_operating_conditions(json_data):
    return operating_conditions_decoder(
        json_data['operatingConditions'] if 'operatingConditions' in json_data else {})


class ProductImporter:
    def __init__(self, model_class, part_type, generate_description):
        self.model_class = model_class
        self.part_type = part_type
        self.generate_description = generate_description
        self.parameters_todo = []

    def get_part(self, manufacturer, part_number):
        try:
            return self.model_class.objects.get(manufacturer=manufacturer, MPN=part_number)
        except self.model_class.DoesNotExist as e:
            return None

    def create_part(self, manufacturer, part_number, json_data):
        logger.info(f"Creating {part_number}")
        common_parameters = self.decode_common_part_parameters(json_data)
        parameters = self.decode_parameters(json_data['parameters'])

        try:
            part = self.model_class(MPN=part_number,
                                    manufacturer=manufacturer,
                                    operating_conditions=decode_operating_conditions(json_data),
                                    storage_conditions=decode_storage_conditions(json_data),
                                    **common_parameters,
                                    **parameters)
        except Exception as e:
            logger.error(f"Creating part error {repr(e)}, {json_data}")
            return None

        try:
            part.description = self.description(part, json_data)
            logger.info(f"Imported {part_number}")
        except Exception as e:
            logger.error(f"Exception during description generation {repr(e)}, {json_data}")
            return None
        return part

    def description(self, part, json_data):
        try:
            description = None
            if self.generate_description == GenerateDescriptionPolicy.AlwaysGenerateDescription:
                description = part.generate_description()
            elif self.generate_description == GenerateDescriptionPolicy.GenerateDescriptionIfMissing:
                if 'description' in json_data and len(json_data['description']) > 0:
                    description = json_data['description'] if 'description' in json_data else None
                else:
                    description = part.generate_description()
            elif self.generate_description == GenerateDescriptionPolicy.AlwaysUseFileDescription:
                description = json_data['description'] if 'description' in json_data else None
            logger.info(f"Generated description {part.description}")
            return description
        except Exception as e:
            logger.error(f"Exception during description generation {repr(e)}, {json_data}")
            return None

    def add_series(self, manufacturer, json_data) -> ProductSeries | None:
        if 'series' in json_data and 'name' in json_data['series']:
            generic = True if 'generic' in json_data['series'] and json_data['series']['generic'] else None
            product_series, created = ProductSeries.objects.get_or_create(
                name=json_data['series']['name'],
                description=json_data['series']['description'] if 'description' in json_data['series'] else None,
                manufacturer=None if generic else manufacturer
            )
            return product_series
        return None

    def decode_common_part_parameters(self, json_data):
        product_type_key = 'partType' if 'partType' in json_data else 'productType'
        common_parameters = {
            'part_type': Product.product_type_from_str(json_data[product_type_key]),
        }
        if 'markingCode' in json_data and json_data['markingCode'] is not None and len(json_data['markingCode']):
            common_parameters['device_marking_code'] = json_data['markingCode']
        if 'productUrl' in json_data and json_data['productUrl'] is not None and len(json_data['productUrl']):
            common_parameters['product_url'] = json_data['productUrl']
        if 'notes' in json_data and json_data['notes'] is not None and len(json_data['notes']):
            common_parameters['notes'] = json_data['notes']
        return common_parameters

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