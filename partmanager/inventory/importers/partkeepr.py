from inventory.models import InventoryPosition, StorageLocation, Category
from invoices.models import Invoice, InvoiceItem
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from .importer_base import InventoryImporterBase
import requests
from decimal import Decimal
from requests.auth import HTTPBasicAuth
import time
import sys
import json


class Partkeepr(InventoryImporterBase):
    def __init__(self, config, debug=False, noEdit=False):
        self.config = config
        self.debug = debug
        self.noEdit = noEdit
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        self.log = open("partkeepr_" + timestr + ".log", 'w')

    def __del__(self):
        self.log.close()

    def find_invoice_item(self, parameters, part_name):
        if 'Invoice Number' in parameters:
            invoice = Invoice.get_by_invoice_number(parameters['Invoice Number']['value'])
            if invoice:
                #print(invoice)
                if len(invoice) == 1:
                    items = invoice[0].invoiceitem_set.filter(distributor_number__contains=part_name)
                    #print(items)
                    if len(items) == 1:
                        print("Found invoice item:", items[0])
                        return items[0]
            print("Unable to find invoice:", parameters['Invoice Number'])

   # def update_inventory_from_partkeepr(self, partkeepr_part, manufacturer_order_number_model):
        #print(partkeepr_part)
   #     if 'storageLocation' in partkeepr_part:
   #         if partkeepr_part['storageLocation'] != 'awaiting order':
   #             parameters = partkeepr_part['parameters']
   #             if 'Invoice Number' in parameters:
   #                 invoice_data = {"Invoice Number": parameters['Invoice Number']['value'], "Position": None,
   #                                 "Symbol": None}
   #             else:
   #                 invoice_data = None
   #             storage_data = {"Quantity": partkeepr_part['stockLevel'], "Location name": partkeepr_part['storageLocation']}
   #             self.update_inventory(manufacturer_order_number_model[0], invoice_data, storage_data)
                # location = StorageLocation.get_by_name(partkeepr_part['storageLocation'])
                # if location is None:
                #     location = StorageLocation(location=partkeepr_part['storageLocation'])
                #     location.save()
                # invoice_item = self.find_invoice_item(partkeepr_part['parameters'], partkeepr_part['name'])
                # inventory_position = InventoryPosition(part=manufacturer_order_number_model[0],
                #                                        storage_location=location,
                #                                        stock=int(partkeepr_part['stockLevel']),
                #                                        invoice=invoice_item,
                #                                        category=Category.get_root())
                # inventory_position.save()
        #print(partkeepr_part)
        #pass

    def get_components(self):
        params = {"itemsPerPage": 9999}
        r = self.api_call('get', '/api/parts', params=params)
        rj = r.json()

        with open('partkeepr.json', 'w') as outputfile:
            json.dump(rj, outputfile, sort_keys=True, indent=4)

        found_count = 0
        not_found_count = 0
        for part in rj["hydra:member"]:
            decoded = self.decode_part(part)
            #print(decoded)
            if len(decoded['manufacturers']) == 1:
                self.create_or_update_storage_location({'name': decoded['storage_location'], 'description': None})
                decoded['manufacturer'] = None
                decoded['part'] = {'manufacturer': decoded['manufacturers'][0]['name'],
                                   'order_number': decoded['manufacturers'][0]['partNumber']}
                invoice_number_str = decoded['invoice']['invoice_number'] if decoded['invoice'] else ''
                decoded['note'] += " Auto import from partkeepr. Partkeepr id: {}, storage location: {}, invoice no.: {}".format(
                    decoded['partkeepr_id'],
                    decoded['storage_location'],
                    invoice_number_str)
                self.create_or_update_inventory_position(decoded)
                #found = ManufacturerOrderNumber.objects.all().filter(manufacturer_order_number=decoded["manufacturers"][0]["partNumber"])
                #if found:
                #    found_count = found_count + 1
                #    print("*** Found MON ->", decoded['name'], decoded["manufacturers"], decoded['description'], invoice_number_str)
                #    self.update_inventory_from_partkeepr(decoded, found)
                #else:
                #    found = Part.objects.all().filter(
                #        manufacturer_part_number__icontains=decoded["manufacturers"][0]['partNumber'][:-1])
                #    if found:
                #        print("Found MPN ->", decoded['name'], decoded["manufacturers"])
                #    else:
                #    print("\tNOT Found", decoded['name'], decoded["manufacturers"], decoded['description'], invoice_number_str)
                #    not_found_count = not_found_count + 1
            elif len(decoded['manufacturers']) == 0:
                print("Adding part to inventory:", decoded)
                self.create_or_update_storage_location({'name': decoded['storage_location'], 'description': None})
                decoded['manufacturer'] = None
                decoded['part'] = {'manufacturer': 'Unknown',
                                   'order_number': decoded['name']}
                invoice_number_str = decoded['invoice']['invoice_number'] if decoded['invoice'] else ''
                decoded['note'] += " Auto import from partkeepr, invoice no.:" + invoice_number_str
                self.create_or_update_inventory_position(decoded)
            else:
                not_found_count += 1
                print("Incorrect manufacturer lentgh:", len(decoded['manufacturers']), "for part:", decoded['name'])
        print(found_count, not_found_count, len(rj["hydra:member"]))

    def decode_part(self, part):
        try:
            footprint_name = part["footprint"]["name"]
        except:
            footprint_name = ""

        storage_location = None
        if 'storageLocation' in part:
            if part['storageLocation']:
                storage_location = part['storageLocation']['name']

        parameters = self.decode_parameters(part["parameters"], part['name'])
        if 'Invoice Number' in parameters:
            invoice_item = self.find_invoice_item(parameters, part['name'])
            invoice_data = {"invoice_number": parameters['Invoice Number']['value'],
                            "invoice_position": invoice_item.position_in_invoice if invoice_item else None}
        else:
            invoice_data = None

        category_dict = None
        if 'category' in part:
            #print(part['category'])
            parent = None
            if 'parent' in part['category'] and part['category']['parent'] is not None:
                parent = part['category']['parent']['name']
            if parent == 'Root Category':
                parent = 'Root'
            category_path = part['category']['categoryPath']
            category_path = category_path.replace('Root Category', 'Root').split(' \u27a4 ')
            category_dict = {'name': part['category']['name'] if part['category']['name'] != 'Root Category' else 'Root',
                             'parent': parent, 'path': category_path}
            self.add_or_update_category(category_dict)
        decoded = {'name': part['name'],
                   "description": part["description"],
                   'part': None,
                   "attachments": self.decode_attachments(part["attachments"]),
                   "note": part["comment"],
                   "condition": 'k',
                   "status": 'b',
                   "footprint": footprint_name,
                   "manufacturers": self.decode_manufacturers(part["manufacturers"]),
                   "productionRemarks": part["productionRemarks"],
                   'partkeepr_id': part['@id'],
                   "storage_location": storage_location,
                   'stock': part['stockLevel'],
                   "parameters": parameters,
                   'invoice': invoice_data,
                   "category": category_dict,
                   'archived': False}
        return decoded

    def decode_manufacturers(self, manufacturers):
        decoded = []
        for manufacturer in manufacturers:
            try:
                decoded.append({"name": manufacturer["manufacturer"]['name'], "partNumber": manufacturer["partNumber"]})
            except TypeError:
                decoded.append({"name": "", "partNumber": ""})
        return decoded

    def decode_attachments(self, attachments):
        decoded = []
        for attachment in attachments:
            decoded.append({"filename": attachment["originalFilename"],
                            "url": self.config["partkeepr"]["url"] + attachment["@id"] + "/getFile",
                            'description': attachment["description"]})
        return decoded

    def decode_parameters(self, parameters, partname):
        decoded = {}
        for parameter in parameters:
            if parameter["valueType"] == "string":
                decoded[parameter["name"]] = {"value": parameter["stringValue"]}
            elif parameter["valueType"] == "numeric":
                if parameter["unit"] is not None:
                    if parameter["maxSiPrefix"] is not None:
                        maxValue = Decimal(str(parameter["maxValue"])) * Decimal(
                            parameter["maxSiPrefix"]["base"]) ** Decimal(parameter["maxSiPrefix"]["exponent"])
                    else:
                        maxValue = Decimal(str(parameter["maxValue"])) if parameter["maxValue"] is not None else None
                    if parameter["minSiPrefix"] is not None:
                        minValue = Decimal(str(parameter["minValue"])) * Decimal(
                            parameter["minSiPrefix"]["base"]) ** Decimal(parameter["minSiPrefix"]["exponent"])
                    else:
                        minValue = Decimal(str(parameter["minValue"])) if parameter["minValue"] is not None else None
                    if parameter["siPrefix"] is not None:
                        value = Decimal(str(parameter["value"])) * Decimal(parameter["siPrefix"]["base"]) ** Decimal(
                            parameter["siPrefix"]["exponent"])
                    else:
                        value = Decimal(str(parameter["value"])) if parameter["value"] is not None else None
                    decoded[parameter["name"]] = {"value": value, "valueMin": minValue, "valueMax": maxValue,
                                                  "unit": parameter["unit"]["name"]}
                else:
                    value = Decimal(str(parameter["value"])) if parameter["value"] is not None else None
                    maxValue = Decimal(str(parameter["maxValue"])) if parameter["maxValue"] is not None else None
                    minValue = Decimal(str(parameter["minValue"])) if parameter["minValue"] is not None else None
                    decoded[parameter["name"]] = {"value": value, "valueMax": maxValue, "valueMin": minValue}
                    #print(parameter)
            else:
                raise
        return decoded

    def api_call(self, method, url, **kwargs):
        """calls Partkeepr API
        :method: requst method
        :url: part of the url to call (without base)
        :data: tata to pass to the request if any
        :returns: requests object
        """

        if self.noEdit and method != 'get':
            return
        pk_user = self.config["partkeepr"]["user"]
        pk_pwd = self.config["partkeepr"]["pwd"]
        pk_url = self.config["partkeepr"]["url"]
        try:
            r = requests.request(
                method,
                pk_url + url,
                **kwargs,
                auth=HTTPBasicAuth(pk_user, pk_pwd),
                verify=False
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        return r


