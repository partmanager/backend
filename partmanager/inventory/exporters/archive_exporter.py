import shutil
from .directory_exporter import export as directory_export


def export(inventory_positions, workdir=None):
    workdir = directory_export(inventory_positions, workdir)
    shutil.make_archive(workdir, 'zip', root_dir=workdir)
    return workdir + '.zip'