from partcatalog.models.fields.resolution import Resolution


def resolution_decoder(json_data):
    value = json_data
    if value:
        resolution = Resolution()
        resolution.width = int(value['width'])
        resolution.height = int(value['height'])
        return resolution
