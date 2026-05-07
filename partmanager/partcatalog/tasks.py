from pathlib import Path
from partsdb_tools.components.Part import part_from_dict
from partsdb_tools.detail.file_operations import load_json
from json.decoder import JSONDecodeError
from django.conf import settings
from .importers.part_database_importer import import_form_file
from .importers.part_importer import import_part
from .generators.generic_resistor_generator import generate_generic_resistors


def import_components(parts_to_import, progress_recorder=None):
    progress_bar_max = 4 + len(parts_to_import)
    for i, file in enumerate(parts_to_import):
        try:
            print(f"importing {file}")
            if progress_recorder:
                progress_recorder.set_progress(i + 4, progress_bar_max, description=f'Importing components from {file}')
            import_form_file(file, dry=False)
        except JSONDecodeError as e:
            print(f"import error {e}")


def generate_generic_parts():
    generate_generic_resistors()

def partsdb_directory_import():
    partsdb_settings = settings.PARTSDB_CONFIG
    for local_dir in partsdb_settings["local_dir"]:
        source = Path(partsdb_settings['local_dir'][local_dir]['dir'])
        for part_file in source.glob("*.json"):
            part = part_from_dict(load_json(part_file), part_file)
            if import_part(part):
                print("Success")

