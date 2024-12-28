import json
import os
from .invoice_importer_base import InvoiceImporterBase


class DirectoryInvoiceImporter(InvoiceImporterBase):
    def __process_invoice_file(self, invoice_filename, files_dir):
        print("Importing invoice", invoice_filename)
        with open(invoice_filename, 'r') as invoice_file:
            invoice = json.load(invoice_file)
            self.import_invoice_from_dict(invoice, files_dir)

    def import_invoice(self, workdir):
        for invoice_file in os.listdir(workdir):
            if invoice_file.endswith('.json'):
                self.__process_invoice_file(workdir.joinpath(invoice_file), workdir.joinpath('files'))
