import shutil
from . import directory_exporter


def export(invoices, workdir=None):
    workdir = directory_exporter.export(invoices, workdir)
    shutil.make_archive(workdir, 'zip', root_dir=workdir)
    return workdir + '.zip'
