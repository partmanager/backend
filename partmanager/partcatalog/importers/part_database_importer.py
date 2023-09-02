from pathlib import Path
from .csv_to_json import CSVToJson
from .json_importer import json_importer
import logging

logger = logging.getLogger('partcatalog')


def import_parts(path, dry=False):
    import_baluns(path + '/baluns', dry=dry)
    import_battery(path + '/batteries', dry=dry)
    import_battery_holder(path + '/battery holders', dry=dry)
    import_bridge_rectifiers(path + '/bridge rectifier', dry=dry)
    #import_capacitors(path + '/capacitors', dry=dry)
    import_common_mode_chokes(path + '/common mode chokes', dry=dry)
    import_connectors(path + '/connectors', dry=dry)
    import_crystals(path + '/crystal', dry=dry)
    import_crystal_oscillators(path + '/crystal oscillators', dry=dry)
    import_diodes(path + '/diodes', dry=dry)
    import_displays(path + '/displays', dry=dry)
    import_enclosures(path + '/enclosures', dry=dry)
    import_esd_supperssors(path + '/ESD Suppressors', dry=dry)
    import_ferrite_beads(path + '/ferrite beads', dry=dry)
    import_fuses(path + '/fuse', dry=dry)
    import_inductors(path + '/inductors', dry=dry)
    import_integrated_circuits(path + '/IC', dry=dry)
    import_light_pipes(path + '/lightpipes', dry=dry)
    import_modules(path + '/modules', dry=dry)
    import_ptc_fuses(path + '/PTC fuse', dry=dry)
    import_relays(path + '/relays', dry=dry)
    #import_resistors(path + '/resistors', dry=dry)
    import_resistor_arrays(path + '/resistor arrays', dry=dry)
    import_surge_arresters(path + '/surge arresters', dry=dry)
    import_transistors_bipolar(path + '/transistors/bipolar', dry=dry)
    import_transistors_mosfet(path + '/transistors/mosfet', dry=dry)
    import_tvs(path + '/TVS', dry=dry)
    import_varistor(path + "/varistors", dry=dry)


def import_baluns(path, dry=True):
    import_csv_files(path, 'balun', dry=dry)
    import_json_files(path, 'balun', dry=dry)


def import_battery(path, dry=True):
    import_csv_files(path, 'batteries', dry=dry)
    import_json_files(path, 'batteries', dry=dry)


def import_battery_holder(path, dry=True):
    import_csv_files(path, 'battery holders', dry=dry)
    import_json_files(path, 'battery holders', dry=dry)


def import_bridge_rectifiers(path, dry=True):
    import_csv_files(path, 'bridge rectifiers', dry=dry)
    import_json_files(path, 'bridge rectifiers', dry=dry)


def import_capacitors(path, dry=True):
    import_csv_files(path, 'capacitors', dry=dry)
    import_json_files(path, 'capacitors', dry=dry)


def import_common_mode_chokes(path, dry):
    import_csv_files(path, 'common mode chokes', dry=dry)
    import_json_files(path, 'common mode chokes', dry=dry)


def import_connectors(path, dry):
    import_csv_files(path, 'connectors', dry=dry)
    import_json_files(path, 'connectors', dry=dry)


def import_crystals(path, dry):
    import_csv_files(path, 'crystals', dry=dry)
    import_json_files(path, 'crystals', dry=dry)


def import_crystal_oscillators(path, dry):
    import_csv_files(path, 'crystal oscillators', dry=dry)
    import_json_files(path, 'crystal oscillators', dry=dry)


def import_diodes(path, dry):
    import_csv_files(path, 'diodes', dry=dry)
    import_json_files(path, 'diodes', dry=dry)


def import_displays(path, dry):
    import_csv_files(path, 'displays', dry=dry)
    import_json_files(path, 'displays', dry=dry)


def import_enclosures(path, dry):
    import_csv_files(path, 'enclosures', dry=dry)
    import_json_files(path, 'enclosures', dry=dry)


def import_esd_supperssors(path, dry):
    import_csv_files(path, 'ESD Suppressos', dry=dry)
    import_json_files(path, 'ESD Suppressos', dry=dry)


def import_ferrite_beads(path, dry):
    import_csv_files(path, 'Ferrite beads', dry=dry)
    import_json_files(path, 'Ferrite beads', dry=dry)


def import_fuses(path, dry):
    import_csv_files(path, 'fuses', dry=dry)
    import_json_files(path, 'fuses', dry=dry)


def import_inductors(path, dry):
    import_csv_files(path, 'inductors', dry=dry)
    import_json_files(path, 'inductors', dry=dry)


def import_integrated_circuits(path, dry):
    import_csv_files(path, 'IC', dry=dry)
    import_json_files(path, 'IC', dry=dry)


def import_light_pipes(path, dry):
    import_csv_files(path, 'light pipes', dry=dry)
    import_json_files(path, 'light pipes', dry=dry)


def import_modules(path, dry):
    import_csv_files(path, 'modules', dry=dry)
    import_json_files(path, 'modules', dry=dry)


def import_ptc_fuses(path, dry):
    import_csv_files(path, 'PTC fuses', dry=dry)
    import_json_files(path, 'PTC fuses', dry=dry)


def import_relays(path, dry):
    import_csv_files(path, 'relays', dry=dry)
    import_json_files(path, 'relays', dry=dry)


def import_resistors(path, dry):
    import_csv_files(path, 'resistors', dry=dry)
    import_json_files(path, 'resistors', dry=dry)


def import_resistor_arrays(path, dry):
    import_csv_files(path, 'resistor arrays', dry=dry)
    import_json_files(path, 'resistor arrays', dry=dry)


def import_surge_arresters(path, dry):
    import_csv_files(path, 'surge arresters', dry=dry)
    import_json_files(path, 'surge arresters', dry=dry)


def import_transistors_bipolar(path, dry):
    from .transistor_bipolar_csv_importer import parts_import
    parts_import(path + '/transistors.csv')
    parts_import(path + '/diodes incorporated/diodes_incorporated.csv')
    #import_csv_files(path, 'bipolar transistors', dry=dry)
    #import_json_files(path, 'bipolar transistors', dry=dry)


def import_transistors_mosfet(path, dry):
    import_csv_files(path, 'transistors mosfet', dry=dry)
    import_json_files(path, 'transistors mosfet', dry=dry)


def import_tvs(path, dry):
    from .tvs_csv_importer import parts_import
    #parts_import(path + '/diodes_incorporated_SMAJ.csv')
    parts_import(path + '/diotec_semiconductor_P4SMAJ.csv')
    parts_import(path + '/onsemi.csv')
    parts_import(path + '/on_semiconductor.csv')
    parts_import(path + '/stmicroelectronics.csv')
    parts_import(path + '/vishay.csv')


def import_varistor(path, dry):
    import_csv_files(path, 'varistors', dry=dry)
    import_json_files(path, 'varistors', dry=dry)


def import_csv_files(path, name, dry=True):
    logger.info('================================================')
    logger.info(f"Importing {name} from {path}")
    print(f"Importing {name} from {path}")
    importer = CSVToJson()
    for file in Path(path).rglob('*.csv'):
        try:
            logger.info(f"Loading {file}")
            print(f"Loading {file}")
            importer.parts_load(file)
        except KeyError as e:
            logger.error(f"Invalid file {file} {e}")
    importer.export('/tmp/' + name + '.json')
    importer.run(dry=dry)
    return importer


def import_json_files(path, name, dry=True):
    logger.info('================================================')
    logger.info(f"Importing {name} from {path}")
    for file in Path(path).rglob('*.json'):
        try:
            logger.info(f"Loading {file}")
            json_importer.parts_import(file)
            json_importer.run(dry=dry)
        except KeyError as e:
            logger.error(f"Invalid file {file} {e}")
