from celery import shared_task
from django.conf import settings
from .importers.part_database_importer import import_parts


@shared_task
def import_components():
    print('importing parts from partsdb')
    part_database_path = settings.PARTSDB_DIRECTORY
    import_parts(part_database_path + 'parts')
