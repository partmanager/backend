import csv
from decimal import Decimal
from .invoice_importer_base import InvoiceImporterBase
from distributors.models import Distributor


class TMECSVImporter(InvoiceImporterBase):
    distributor = None

    def import_invoice(self, filename):
        if self.distributor is None:
            self.distributor = Distributor.get_by_name('TME')

        with open(filename, 'r') as file:
            file_content = ''
            for line in file:
                file_content = file_content + line

            reader = csv.DictReader(file_content.splitlines(), delimiter=';')
            self._process_rows(reader)
        return True

    def _process_rows(self, rows):
        invoices_items = []
        for row in rows:
            invoice_model = self.get_or_create_invoice_from_row(row)

            for quantity_field in row:
                if quantity_field.rstrip() in ["Ilość zamówiona", "Ilośćzamówiona", "Ordered quantity"]:
                    ordered_quantity = Decimal(row[quantity_field])
            if "Wartość pozycji netto" in row:
                net_price = Decimal(row["Wartość pozycji netto"].replace(',', '.'))
            elif 'Net item value' in row:
                net_price = Decimal(row["Net item value"].replace(',', '.'))
            elif "Wartość pozycji brutto" in row:
                gross_price = Decimal(row["Wartość pozycji brutto"].replace(',', '.'))
                net_price = gross_price / Decimal('1.23')
            elif "Gross item value" in row:
                gross_price = Decimal(row["Gross item value"].replace(',', '.'))
                net_price = gross_price / Decimal('1.23')

            if 'Numer faktury' in row:
                invoice_item_dict = {'order_number': row['Numer zamówienia'],
                                     'position': row["Numer pozycji"],
                                     'distributor_number': row['Symbol TME'],
                                     'ordered_quantity': ordered_quantity,
                                     'shipped_quantity': ordered_quantity,
                                     "unit": row["Jednostka"],
                                     'price': {'net': net_price,
                                               'vat_tax': '23',
                                               'currency_display': row['Waluta']},
                                     'invoice_model': invoice_model}
            elif 'Invoice number' in row:
                invoice_item_dict = {'order_number': row['Order number'],
                                     'position': row["Item no."],
                                     'distributor_number': row['TME Symbol'],
                                     'ordered_quantity': ordered_quantity,
                                     'shipped_quantity': ordered_quantity,
                                     "unit": row["Unit"],
                                     'price': {'net': net_price,
                                               'vat_tax': '23',
                                               'currency_display': row['Currency']},
                                     'invoice_model': invoice_model}
            else:
                raise
            invoices_items.append(invoice_item_dict)
        self.update_or_create_items(self.distributor, invoices_items)

    def get_or_create_invoice_from_row(self, csv_row):
        if 'Numer faktury' in csv_row:
            invoice_dict = {'invoice_number': csv_row['Numer faktury'],
                            'invoice_date': csv_row['Data wystawienia']
                            }
        elif 'Invoice number' in csv_row:
            invoice_dict = {'invoice_number': csv_row['Invoice number'],
                            'invoice_date': csv_row['Date of issue']
                            }
        else:
            raise
        return self.get_or_create_invoice(self.distributor, invoice_dict, None)



