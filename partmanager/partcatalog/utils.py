from .models.part import Part
from .models.manufacturer_order_number import ManufacturerOrderNumber
from manufacturers.models import Manufacturer, get_manufacturer_by_name


def get_part(manufacturer, manufacturer_part_number, manufacturer_order_number, translate_manufacturer_name=None):
    if not isinstance(manufacturer, Manufacturer):
        if translate_manufacturer_name:
            manufacturer = get_manufacturer_by_name(translate_manufacturer_name(manufacturer))
        else:
            manufacturer = get_manufacturer_by_name(manufacturer)

    if manufacturer:
        found_order_number = []
        found_part = None

        if manufacturer_order_number:
            found_order_number = ManufacturerOrderNumber.objects.all().filter(manufacturer=manufacturer,
                                                                              manufacturer_order_number=manufacturer_order_number)
        if len(found_order_number) == 0:
            if manufacturer_part_number is None:
                manufacturer_part_number = manufacturer_order_number
            found_part = Part.objects.all().filter(manufacturer=manufacturer, manufacturer_part_number=manufacturer_part_number)
            if len(found_part) == 0:
                found_part = Part.objects.all().filter(manufacturer=manufacturer,
                                                       manufacturer_part_number=manufacturer_part_number+'#')
        elif len(found_order_number) == 1:
            found_part = [found_order_number[0].part]

        print("Searching part:", manufacturer_part_number, " \tfound manufacturer:", manufacturer.name if manufacturer else "No",
              "\tMON:", found_order_number[0] if len(found_order_number) == 1 else "None")
        if found_order_number:
            return {'mpn': found_part[0], 'mon': found_order_number[0]}
        if found_part:
            return {'mpn': found_part[0], 'mon': None}
    else:
        print("Unable to find manufacturer:", manufacturer, 'for part', manufacturer_part_number, "mpn: ", manufacturer_order_number)
