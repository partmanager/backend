import json
import time
import os
import shutil
from .invoice_importer_base import InvoiceImporterBase


class ArchiveInvoiceImporter(InvoiceImporterBase):
    def __process_invoice_file(self, invoice_filename):
        print("Importing invoice", invoice_filename)
        with open(invoice_filename, 'r') as invoice_file:
            invoice = json.load(invoice_file)
            self.import_invoice_from_dict(invoice)

    def import_invoice(self, archive_file):
        workdir = '/tmp/invoice_import/' + time.strftime("%Y%m%d-%H%M%S")
        os.makedirs(workdir)
        archive_filename = workdir + '/' + archive_file.name
        with open(archive_filename, 'wb') as file:
            file.write(archive_file.read())
        shutil.unpack_archive(archive_filename, extract_dir=workdir)
        for invoice_file in os.listdir(workdir):
            if invoice_file.endswith('.json'):
                self.__process_invoice_file(workdir + '/' + invoice_file)
        return True
