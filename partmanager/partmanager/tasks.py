import shutil
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from distributors.importers.directory_importer import import_distributor
from invoices.importers.directory_importer import DirectoryInvoiceImporter
from manufacturers.importers.directory_importer import import_manufacturers
from inventory.importers.directory_importer import DirectoryImporter
from projects.importers.directory_importer import import_project


@shared_task(bind=True)
def import_data(self, archive_filename, workdir):
    progress_recorder = ProgressRecorder(self)

    progress_recorder.set_progress(1, 6, description='Decompressing import data file')
    shutil.unpack_archive(archive_filename, extract_dir=workdir)

    progress_recorder.set_progress(2, 6, description='Importing manufacturers')
    import_manufacturers(workdir + '/manufacturers')

    progress_recorder.set_progress(3, 6, description='Importing distributors')
    import_distributor(workdir + '/distributors')

    progress_recorder.set_progress(4, 6, description='Importing invoices')
    importer = DirectoryInvoiceImporter()
    importer.dry = False
    importer.import_invoice(workdir + '/invoices')

    progress_recorder.set_progress(5, 6, description='Importing inventories')
    DirectoryImporter().import_inventory(workdir + '/inventory')

    progress_recorder.set_progress(6, 6, description='Importing projects')
    import_project(workdir + '/projects')
