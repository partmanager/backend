from pathlib import Path
from .csv_to_json import CSVToJson
from .json_importer import json_importer


def import_test_parts(path, dry=False):
    json_importer.parts_import(path + '/test_data/json/test_balun.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_batteries.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_battery_holders.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_bridge_rectifiers.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_capacitors.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_common_mode_chokes.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_crystal_oscillators.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_crystals.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_connectors.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_diodes.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_displays.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_enclosures.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_ESD_suppressors.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_ferrite_beads.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_fuses.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_inductors.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_light_pipes.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_modules.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_PTC_fuses.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_relays.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_resistors.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_resistor_arrays.json')
    json_importer.run(dry=dry)

    json_importer.parts_import(path + '/test_data/json/test_surge_arresters.json')
    json_importer.run(dry=dry)
