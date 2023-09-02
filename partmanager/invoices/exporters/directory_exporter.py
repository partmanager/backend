import time
import os
import shutil


def create_invoice_file(invoice, filename):
    with open(filename, 'w') as invoice_file:
        invoice_file.write(invoice.to_json())


def copy_invoice_files(invoice, destination):
    if invoice.invoice_file:
        shutil.copy(invoice.invoice_file.path, destination)


def export(invoices, workdir=None):
    if workdir is None:
        workdir = '/tmp/invoice_export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    os.makedirs(workdir + '/files')
    for invoice in invoices:
        filename = "{}_{}.json".format(invoice.distributor.name, invoice.number.replace('/', '_'))
        create_invoice_file(invoice, workdir + '/' + filename)
        copy_invoice_files(invoice, workdir + '/files')
    return workdir
