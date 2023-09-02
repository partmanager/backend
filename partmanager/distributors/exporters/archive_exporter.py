import shutil
from . import directory_exporter


def export(distributors, workdir=None):
    workdir = directory_exporter.export(distributors, workdir)
    shutil.make_archive(workdir, 'zip', root_dir=workdir)
    return workdir + '.zip'
