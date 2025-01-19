from partcatalog.models.fields.storage_conditions import StorageConditions
from partcatalog.models.choices import MSLevel
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __temperature_decode
from .humidity_decoder import relative_humidity_decode as __relative_humidity_decode


def storage_conditions_decoder(json_data):
    temperature = None
    humidity = None
    if 'temperature' in json_data:
        temperature = parameter_str_to_dict(json_data['temperature'], __temperature_decode)
    if 'humidity' in json_data:
        humidity = parameter_str_to_dict(json_data['humidity'], __relative_humidity_decode)

    storage_conditions = StorageConditions()
    if temperature:
        assert temperature['typ'] is None, temperature
        storage_conditions.temperature_min = temperature['min']
        storage_conditions.temperature_max = temperature['max']
    else:
        storage_conditions.temperature_min = None
        storage_conditions.temperature_max = None
    if humidity:
        assert humidity['typ'] is None, humidity
        storage_conditions.humidity_min = humidity['min']
        storage_conditions.humidity_max = humidity['max']
    else:
        storage_conditions.humidity_min = None
        storage_conditions.humidity_max = None
    if 'MSLevel' in json_data and json_data['MSLevel'] is not None:
        storage_conditions.msl_level = MSLevel.from_string(json_data['MSLevel'])
    else:
        storage_conditions.msl_level = None
    return storage_conditions
