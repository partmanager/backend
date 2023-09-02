import decimal


def decimal_decoder(json_data):
    if 'value' in json_data and len(json_data['value']):
        return decimal.Decimal(json_data['value'])
