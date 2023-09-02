from partcatalog.models.fields.backlight import Backlight


def backlight_decoder(json_data):
    value = json_data
    if value:
        backlight = Backlight()
        backlight.source = value['source']
        backlight.color = value['color']
        return backlight
