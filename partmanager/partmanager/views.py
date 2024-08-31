from django.http import FileResponse
import os
import time
import shutil
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from distributors.models import Distributor
from distributors.importers.directory_importer import import_distributor
from distributors.exporters.directory_exporter import export as distributors_export
from inventory.models import InventoryPosition, StorageLocation, Category
from inventory.exporters.directory_exporter import export as inventory_export
from invoices.models import Invoice
from invoices.importers.directory_importer import DirectoryInvoiceImporter
from invoices.exporters.directory_exporter import export as invoices_export
from manufacturers.models import Manufacturer
from manufacturers.importers.directory_importer import import_manufacturers
from manufacturers.exporters.directory_exporter import export as manufacturers_export
from inventory.importers.directory_importer import DirectoryImporter
from projects.models import ProjectVersion
from projects.importers.directory_importer import import_project
from projects.exporters.directory_exporter import export as projects_export
from .tasks import import_data
from partdb_git.tasks import update_all
from symbolandfootprint.tasks import generate_symbols


class ImportView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, format=None):
        import_file = request.FILES['file']
        print(import_file)
        workdir = '/tmp/shelftracker/import/' + time.strftime("%Y%m%d-%H%M%S")
        os.makedirs(workdir)
        archive_filename = workdir + '/' + import_file.name
        with open(archive_filename, 'wb') as file:
            file.write(import_file.read())
        result = import_data.delay(archive_filename, workdir)

        return Response({'task_id': result.task_id})


class UpdateGitView(APIView):
    def post(self, request, format=None):
        result = update_all.delay()
        return Response({'task_id': result.task_id}, status=200)


class GenerateSymbolsView(APIView):
    def post(self, request, format=None):
        result = generate_symbols.delay()
        return Response({'task_id': result.task_id}, status=200)


def export(request):
    workdir = '/tmp/partcatalog/export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    distributors_export(Distributor.objects.all(), workdir + '/distributors')
    inventory_export(InventoryPosition.objects.all(),
                     StorageLocation.objects.all(),
                     Category.objects.all(),
                     workdir + '/inventory')
    invoices_export(Invoice.objects.all(), workdir + '/invoices')
    manufacturers_export(Manufacturer.objects.all(), workdir + '/manufacturers')
    projects_export(ProjectVersion.objects.all(), workdir + '/projects')

    shutil.make_archive(workdir, 'zip', root_dir=workdir)
    archive = open(workdir + '.zip', 'rb')
    response = FileResponse(archive)
    return response
