import csv
from partcatalog.utils import get_part
from projects.models import ProjectVersion, BOM, BOMItem


def translate_manufacturer_name(manufacturer_name):
    name_translator = {'Murata Manufacturing': 'Murata', 'Royal Ohm': 'Royalohm', 'NXP Semiconductors': 'NXP',
                       "ST Microelectronics": "STMicroelectronics", 'DIODEC SEMICONDUCTOR': 'Diotec Semiconductor',
                       'Sierra': 'Sierra Wireless', 'JB Capacitors Company': 'JB Capacitors'}
    if manufacturer_name in name_translator:
        return name_translator[manufacturer_name]
    return manufacturer_name


def decode_bom_group(row):
    translate = {'Resistors': 'r',
                 'Capacitors': 'c',
                 'Inductors': 'l',
                 'Transistors': 't',
                 'Diodes': 'd',
                 'Integrated Circuits': 'i',
                 'Connectors': 'k',
                 'Modules': 'm'}

    if 'BOMGroup' in row:
        bom_group = row['BOMGroup']
        if bom_group in translate:
            return translate[bom_group]
        elif len(bom_group) > 0:
            print('Unknown bom group', bom_group)
        return 'u'
    else:
        designator = row['Designator'].split(',')[0]
        if designator.startswith('R'):  # Resistors
            return 'r'
        elif designator.startswith('C'):  # Capacitors
            return 'c'
        elif designator.startswith('L') or designator.startswith('FB'):  # Inductors
            return 'l'
        elif designator.startswith('T') or designator.startswith('Q'):  # Transistors
            return 't'
        elif designator.startswith('D'):  # Diodes
            return 'd'
        elif designator.startswith('U') or designator.startswith('IC'):  # Integrated Circuits
            return 'i'
        elif designator.startswith('J'):  # Connectors
            return 'k'
        elif designator.startswith('MOD'):  # Modules
            return 'm'
    return 'u'


def process_row(bom, row):
    quantity = row['Quantity']
    designators = row['Designator']
    if 'Manufacturer Part Number' in row and row['Manufacturer Part Number']:
        part = get_part(manufacturer=row['Manufacturer'],
                        manufacturer_part_number=row['Manufacturer Part Number'],
                        manufacturer_order_number=row['Manufacturer Part Number'],
                        translate_manufacturer_name=translate_manufacturer_name)
        group = decode_bom_group(row)
        if part:
            print(f"\tFound part:", part['mpn'])
            item = BOMItem(bom=bom,
                           quantity=quantity,
                           designators=designators,
                           group=group,
                           part=part['mpn'],
                           manufacturer_order_number=part['mon'])
            item.save()
        else:
            item = BOMItem(bom=bom,
                           quantity=quantity,
                           designators=designators,
                           group=group,
                           part_not_found_fallback={"manufacturer": row['Manufacturer'],
                                                    "mpn": row['Manufacturer Part Number']})
            item.save()

def process_bom_from_file(filename, bom):
    print("Processing BOM file")
    #with open(filename) as csvfile:
        # project = Project(name=filename)
        # project.save()
        # bom = BOM(project=project, name=filename)
        # bom.save()

    csvreader = csv.DictReader(filename)
    for row in csvreader:
        process_row(bom, row)
