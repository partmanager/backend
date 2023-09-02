from partcatalog.models.fields.controller import Controller


def controller_decoder(json_data):
    value = json_data
    if value:
        controller = Controller()
        controller.manufacturer = value['manufacturer']
        controller.part_number = value['part number']
        controller.interface = value['interface']
        return controller
