from celery import shared_task
from django.conf import settings
from .importers.part_database_importer import import_parts, import_form_file
from manufacturers.importers.directory_importer import import_manufacturers
from distributors.importers.directory_importer import import_distributor


def import_components(parts_to_import, progress_recorder):
    progress_bar_max = 4 + len(parts_to_import)
    for i, file in enumerate(parts_to_import):
        print(f"importing {file}")
        progress_recorder.set_progress(i + 4, progress_bar_max, description=f'Importing components from {file}')
        import_form_file(file, dry=False)


@shared_task
def import_all(part_database_path):
    print('importing parts from partsdb')
    part_database_path = settings.PARTSDB_DIRECTORY
    import_manufacturers(part_database_path + 'manufacturers')
    import_distributor(part_database_path + 'distributors')
    import_parts(part_database_path + 'parts')
