import csv
from .importer_base import InventoryImporterBase
from distributors.models import Distributor
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
import logging

logger = logging.getLogger('inventory')


class FileImporter(InventoryImporterBase):
    def add_to_inventory(self, distributor, row):
        invoice_data = {"Invoice Number": row["Invoice Number"], "Position": row["Invoice Position"],
                        "Symbol": row["Distributor Order Number"]}
        storage_data = {"Quantity": row["Quantity"], "Location name": row["Storage Location"]}
        mon = distributor.get_order_number(row["Distributor Order Number"])
        if mon and mon.manufacturer_order_number:
            self.update_inventory(mon.manufacturer_order_number, invoice_data, storage_data)
        else:
            found = ManufacturerOrderNumber.objects.filter(
                manufacturer_order_number=row["Manufacturer Order Number"], manufacturer__name=row['Manufacturer'])
            if len(found) == 1:
                mon = found[0]
                self.update_inventory(mon, invoice_data, storage_data)
        return mon

    def file_import(self, filename, distributor_name):
        logger.info("Updating inventory form invoice file:", filename, "Distributor", distributor_name)
        distributor = Distributor.get_by_name(distributor_name)
        logger.debug(distributor)
        not_found = []
        with open(filename) as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                logger.debug(row)
                status = self.add_to_inventory(distributor, row)
                if status is None:
                    not_found.append(row)
            request = []
            for part in not_found:
                if part not in request:
                    request.append(part["Distributor Order Number"])
            if len(request) > 0 and distributor:
                distributor.request_order_numbers(request)


class InvoiceImporter(InventoryImporterBase):
    def add_to_inventory(self, distributor, row):
        mon = distributor.get_order_number(row["Symbol TME"].strip())
        if mon.manufacturer_order_number:
            invoice_data = {"Invoice Number": row["Numer faktury"], "Position": row["Numer pozycji"],
                            "Symbol": row["Symbol TME"]}
            storage_data = {"Quantity": row["Ilośćzamówiona"], "Location name": "AssemblyBox"}
            self.update_inventory(mon.manufacturer_order_number, invoice_data, storage_data)
        else:
            logger.info("\tMissing MON in DON:", row["Symbol TME"], mon)
        return mon

    def invoice_import(self, filename, distributor_name):
        logger.info("Updating inventory form invoice file:", filename, "Distributor", distributor_name)
        distributor = Distributor.get_by_name(distributor_name)
        logger.debug(distributor)
        not_found = []
        with open(filename) as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=';')
            for row in csvreader:
                logger.debug("Processing:", row["Symbol TME"])
                status = self.add_to_inventory(distributor, row)
                if status is None:
                    not_found.append(row)
            request = []
            for part in not_found:
                if part not in request:
                    request.append(part["Symbol TME"])
            if len(request) > 0:
                distributor.request_manufacturer_order_number(request)
