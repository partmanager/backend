import shutil
from . import directory_exporter


def export(manufacturers, workdir=None):
    workdir = directory_exporter.export(manufacturers, workdir)
    shutil.make_archive(workdir, 'zip', root_dir=workdir)
    return workdir + '.zip'
