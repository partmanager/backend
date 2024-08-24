from partcatalog.models.fields.operating_conditions import OperatingConditions
from .field_decoder_common import parameter_str_to_dict
from .si_unit_decoder import temperature_decode as __temperature_decode
from .humidity_decoder import relative_humidity_decode as __relative_humidity_decode


def operating_conditions_decoder(json_data):
    temperature = None
    humidity = None
    if 'temperature' in json_data:
        temperature = parameter_str_to_dict(json_data['temperature'], __temperature_decode)
    if 'humidity' in json_data:
        humidity = parameter_str_to_dict(json_data['humidity'], __relative_humidity_decode)

    operating_conditions = OperatingConditions()
    if temperature:
        assert temperature['typ'] is None, temperature
        operating_conditions.temperature_min = temperature['min']
        operating_conditions.temperature_max = temperature['max']
    else:
        operating_conditions.temperature_min = None
        operating_conditions.temperature_max = None
    if humidity:
        assert humidity['typ'] is None, humidity
        operating_conditions.humidity_min = humidity['min']
        operating_conditions.humidity_max = humidity['max']
    else:
        operating_conditions.humidity_min = None
        operating_conditions.humidity_max = None
    return operating_conditions
