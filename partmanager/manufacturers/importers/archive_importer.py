import time
import os
import shutil
from .directory_importer import import_manufacturers as import_manufacturers_from_directory


def import_manufacturers(archive_file):
    workdir = '/tmp/manufacturers/import/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    archive_filename = workdir + '/' + archive_file.name
    with open(archive_filename, 'wb') as file:
        file.write(archive_file.read())
    shutil.unpack_archive(archive_filename, extract_dir=workdir)

    import_manufacturers_from_directory(workdir)
