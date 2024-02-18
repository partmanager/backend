import time
import os
import shutil
from .directory_importer import process_distributor_file


def import_distributor(archive_file):
    workdir = '/tmp/distributor/import/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    archive_filename = workdir + '/' + archive_file.name
    with open(archive_filename, 'wb') as file:
        file.write(archive_file.read())
    shutil.unpack_archive(archive_filename, extract_dir=workdir)
    for distributor_file in os.listdir(workdir):
        if distributor_file.endswith('.json'):
            process_distributor_file(workdir + '/' + distributor_file)
