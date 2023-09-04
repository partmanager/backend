from celery import shared_task
from django.conf import settings
from .importers.part_database_importer import import_parts
from manufacturers.importers.directory_importer import import_manufacturers
from distributors.importers.directory_importer import import_distributor


@shared_task
def import_components():
    print('importing parts from partsdb')
    part_database_path = settings.PARTSDB_DIRECTORY
    import_manufacturers(part_database_path + 'manufacturers')
    import_distributor(part_database_path + 'distributors')
    import_parts(part_database_path + 'parts')
