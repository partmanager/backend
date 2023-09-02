import csv
from manufacturers.models import get_manufacturer_by_name
from .common import decode_common_part_parameters, decode_files, add_manufacturer_order_number


class CSVImporterBase:
    def __init__(self, model_class):
        self.last_manufacturer = None
        self.model_class = model_class

    def parts_import(self, filename):
        print("Importing parts from csv file")
        with open(filename) as csvfile:
            csvreader = csv.DictReader(csvfile, dialect='unix')
            for row in csvreader:
                self.add_part(row)

    def add_part(self, dictionary):
        # print(dictionary)
        manufacturer = self.get_manufacturer(dictionary)
        if manufacturer:
            part_number = dictionary['Part Number']
            part = self.get_part(manufacturer, part_number)
            if not part:
                part = self.create_part(manufacturer, part_number, dictionary)
                if part:
                    part.save()
                    file = decode_files(dictionary)
                    for f in file:
                        part.files.add(f)
                    part.save()
                    print(part.manufacturer_part_number, "\tAdd")
            else:
                print(part.manufacturer_part_number, "\tSkip")

            add_manufacturer_order_number(manufacturer, part, dictionary)
        else:
            print("Unknown manufacturer")

    def get_manufacturer(self, dictionary):
        manufacturer_name = dictionary['Manufacturer']
        if self.last_manufacturer:
            if self.last_manufacturer.name == manufacturer_name:
                return self.last_manufacturer
        self.last_manufacturer = get_manufacturer_by_name(manufacturer_name)
        return self.last_manufacturer

    def get_part(self, manufacturer, part_number):
        part = self.model_class.objects.filter(manufacturer=manufacturer, manufacturer_part_number=part_number)
        if len(part) > 0:
            if len(part) == 1:
                return part[0]
            else:
                print("**********************************")
