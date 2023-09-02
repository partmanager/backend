import csv
from decimal import Decimal
from .invoice_importer_base import InvoiceImporterBase
from distributors.models import Distributor
from partmanager.choices import QuantityUnit


class GenericCSVImporter(InvoiceImporterBase):
    unit_translator = {'szt.': QuantityUnit.PCS,
                       'szt': QuantityUnit.PCS,
                       'kg': QuantityUnit.KG,
                       'm': QuantityUnit.M,
                       'm.b': QuantityUnit.M}

    def import_invoice(self, distributor_name, invoice_date, filename):
        self.distributor = Distributor.get_by_name(distributor_name)
        if self.distributor is None:
            raise RuntimeError('Unknown distributor')
        print('Adding invoice from distributor:', self.distributor.name)

        with filename.open() as file:
            file_content = ''
            for line in file:
                file_content = file_content + line.decode()

            #reader = csv.DictReader(file_content.splitlines(), delimiter=';')
            reader = csv.DictReader(file_content.splitlines(), delimiter='\t')
            invoice_list = list(reader)
            invoice_model = self.get_or_create_invoice_from_row(invoice_list[0], invoice_date)
            if invoice_model:
                print('Adding items into invoice', invoice_model.number)
                self._process_rows(invoice_model, invoice_list)
        return invoice_model

    def _process_rows(self, invoice_model, rows):
        invoices_items = []
        for row in rows:
            print('\tProcessing row', row)
            invoice_item_dict = {'order_number': None,
                                 'position': None,
                                 'distributor_number': None,
                                 'ordered_quantity': None,
                                 'shipped_quantity': None,
                                 "unit": None,
                                 'price': {'net_value': None,
                                           'vat_tax': None,
                                           'currency': 'PLN'},
                                 'invoice_model': invoice_model}
            fields_to_validate = {'price': {}}

            for field in row:
                if field in ['Numer faktury']:
                    if invoice_model.number != row[field]:
                        raise
                elif field.upper() in ['LP.']:
                    invoice_item_dict['position'] = int(row[field])
                elif field in ['Symbol']:
                    invoice_item_dict['distributor_number'] = row[field]
                elif field in ['Nazwa']:
                    fields_to_validate['Name'] = row[field]
                elif field in ['Ilość']:
                    invoice_item_dict['ordered_quantity'] = Decimal(row[field].replace(',', '.'))
                    invoice_item_dict['shipped_quantity'] = Decimal(row[field].replace(',', '.'))
                elif field.upper() in ['J.M', 'J.M.']:
                    invoice_item_dict['unit'] = self.unit_translator[row[field]]
                elif field in ['VAT [%]']:
                    invoice_item_dict['price']['vat_tax'] = int(row[field])
                elif field in ['Cena jednostkowa netto']:
                    invoice_item_dict['price']['net_value'] = Decimal(row[field].replace(',', '.'))
                elif field in ['cena jednostkowa brutto']:
                    fields_to_validate['price']['unit_gross_value'] = Decimal(row[field].replace(',', '.'))
                elif field in ['Wartość netto']:
                    fields_to_validate['price']['net_value'] = Decimal(row[field].replace(',', '.'))
                elif field in ['Wartość brutto']:
                    fields_to_validate['price']['gross_value'] = Decimal(row[field].replace(',', '.'))
                elif field in ['Kwota VAT']:
                    fields_to_validate['price']['vat_value'] = Decimal(row[field].replace(',', '.'))
                elif field in ['Waluta']:
                    invoice_item_dict['price']['currency'] = row[field]
                elif field in ['Numer zamówienia']:
                    invoice_item_dict['order_number'] = row[field]
                else:
                    raise TypeError("Unknown Field " + str(field))

            self.validate(invoice_item_dict, fields_to_validate)
            invoices_items.append(invoice_item_dict)
        self.update_or_create_items(self.distributor, invoices_items)

    def validate(self, invoice_item_dict, fields_to_validate):
        return True

    def get_or_create_invoice_from_row(self, csv_row, invoice_date):
        invoice_dict = {'invoice_number': None,
                        'invoice_date': invoice_date,
                        'order_number': None,
                        'order_date': None,
                        'bookkeeping': 'p'}
        for field in csv_row:
            if field in ['Numer faktury']:
                invoice_dict['invoice_number'] = csv_row[field]
            elif field in ['Data wystawienia']:
                invoice_dict['invoice_date'] = csv_row[field]

        if invoice_dict['invoice_number'] is not None:
            return self.get_or_create_invoice(self.distributor, invoice_dict, None)
