from json.decoder import JSONDecodeError
from .importers.part_database_importer import import_form_file
from .generators.generic_resistor_generator import generate_generic_resistors

def import_components(parts_to_import, progress_recorder):
    progress_bar_max = 4 + len(parts_to_import)
    for i, file in enumerate(parts_to_import):
        try:
            print(f"importing {file}")
            progress_recorder.set_progress(i + 4, progress_bar_max, description=f'Importing components from {file}')
            import_form_file(file, dry=False)
        except JSONDecodeError as e:
            print(f"import error {e}")


def generate_generic_parts():
    generate_generic_resistors()