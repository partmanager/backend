def int_decoder(json_data):
    if json_data['value']:
        return int(json_data['value'])