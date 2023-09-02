from .DistributorConnectorBase import *
import requests
from decimal import *
import re
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(o)


class Mouser(DistributorConnectorBase):
    def __init__(self, api_key):
        DistributorConnectorBase.__init__(self, "Mouser", 20)
        self.api_key = api_key
        self.api_url = "https://api.mouser.com/api/v1"
        self.manufacturers_map = {}
        self.cached_capacitors = {}
        self.cached_resistors = {}

    def get_component(self, distributor_order_number):
        """
        :param distributor_order_number: Distributor specific order number as string
        :return: array of components
        """
        response = self.__request_parts_data(distributor_order_number)
        if response:
            response_json = response.json()
            parts = response_json["SearchResults"]['Parts']
            response = []
            for part in parts:
                response.append({'Distributor Order Number': part['MouserPartNumber'],
                                 'DistributorComponentWebPage': ['ProductDetailUrl'],
                                 "Manufacturer": part['Manufacturer'],
                                 'Manufacturer Part Number': part['ManufacturerPartNumber']})
            return response

    def get_stock_and_prices(self, distributor_order_number_set):
        response = self.__request_parts_data(distributor_order_number_set)
        if response:
            response_json = response.json()
            parts = response_json["SearchResults"]['Parts']
            stock_and_price = []
            for part in parts:
                symbol = part['MouserPartNumber']
                stock_count = self.__encode_order_info(part)['StockCount']
                price_list = self.__encode_price_ranges(part['PriceBreaks'])
                stock_and_price.append({'distributorOrderNumber': symbol, 'stockCount': stock_count, 'priceList': price_list})
            return stock_and_price

    def find_component(self, manufacturer_part_number):
        """
        :param manufacturer_part_number: Manufacturer Part Number as string
        :return:
        """
        print("Mouser searching: ", manufacturer_part_number)
        content = {"SearchByPartRequest": {"mouserPartNumber": manufacturer_part_number,
                                           "partSearchOptions": "Exact"}}
        response = requests.post(self.__build_request_url('search', 'partnumber'), json=content)
        if response:
            response_json = response.json()
            parts = response_json["SearchResults"]['Parts']
            result = []
            for part in parts:
                encoded = self.__encode_part(part)
                if encoded['OrderInfo']['StockCount'] > 0 or not self.require_on_stock:
                    result.append(encoded)
            return result

    def __search_by_keyword(self, keyword):
        print(keyword)
        starting_record = 0
        result = []
        while True:
            request_content = {"SearchByKeywordRequest": {"keyword": keyword,
                                                          "records": 50,
                                                          "startingRecord": starting_record,
                                                          "searchOptions": "InStock",
                                                          "searchWithYourSignUpLanguage": "false"
                                                          }
                               }
            response = requests.post(self.__build_request_url('search', 'keyword'), json=request_content)
            print(response)
            if response:
                response_json = response.json()
                parts = response_json["SearchResults"]['Parts']
                starting_record += len(parts)
                for part in parts:
                    encoded = self.__encode_part(part)
                    if encoded['OrderInfo']['StockCount'] > 0 or not self.require_on_stock:
                        result.append(encoded)
                if starting_record >= response_json["SearchResults"]["NumberOfResult"]:
                    break
            else:
                break
        return result

    def __get_capacitance_from_description(self, description):
        match = re.match(r'(.)* ((\d+[.])?\d+[m|u|n|p|f]?F)', description)
        if match:
            capacitance = capacitor.convert_capacitance_co_farads(match.group(2))
            return capacitance

    def __get_resistance_from_description(self, description):
        match = re.match(r'(.)* ((\d+[.])?\d+(([M|K|k|m|u]? ?ohm[s]?)|([M|K|k|m|u]) ))', description)
        if match:
            resistance_string = match.group(2).replace("ohms", "R").replace("ohm", "R")
            resistance = resistor.convert_resistance_to_ohms(resistance_string.rstrip())
            return resistance

    def __encode_part(self, part):
        print(part)
        result = {}
        result["Description"] = part['Description']
        result["Links"] = self.__encode_urls(part)
        result["OrderInfo"] = self.__encode_order_info(part)
        result["Parameters"] = self.__encode_parameters(part)
        result["PriceRanges"] = self.__encode_price_ranges(part['PriceBreaks'])
        result["Distributor Order Number"] = part['MouserPartNumber']
        return result

    @staticmethod
    def __encode_urls(part):
        result = {"ProductInformationPage": part['ProductDetailUrl'], "Datasheet URL": part['DataSheetUrl']}
        return result

    @staticmethod
    def __encode_parameters(part):
        result = {}
        result["Manufacturer"] = part['Manufacturer']
        result["Manufacturer Part Number"] = part['ManufacturerPartNumber']
        for attribute in part["ProductAttributes"]:
            result[attribute['AttributeName']] = attribute['AttributeValue']
        return result

    @staticmethod
    def __encode_price_ranges(price_ranges):
        try:
            result = []
            for price_range in price_ranges:
                price = Decimal(price_range['Price'].replace(',', '.').replace("zł", "").replace(u'\xa0', ""))
                result.append({"amount": price_range['Quantity'], "price": price, "currency": price_range['Currency'],
                               'vatRate': '-', 'priceType': 'NET'})
            return result
        except InvalidOperation:
            print(price_ranges)
            raise

    @staticmethod
    def __encode_order_info(part):
        result = {"MinAmount": int(part['Min']), "Multiples": int(part['Mult'])}
        try:
            result["StockCount"] = int(part['Availability'].replace("In Stock", ""))
        except (ValueError, KeyError):
            result["StockCount"] = 0
        return result

    def __get_manufacturer_list(self):
        response = requests.get(self.__build_request_url('search', 'manufacturerlist'))
        if response:
            response_json = response.json()
            for manufacturer in response_json["MouserManufacturerList"]["ManufacturerList"]:
                self.manufacturers_map[manufacturer["ManufacturerName"]] = manufacturer["ManufacturerId"]

    def __build_request_url(self, action, target):
        url = self.api_url + "/" + action + "/" + target + "?apiKey=" + self.api_key
        return url

    def __request_parts_data(self, distributor_order_number):
        mouser_part_number_str = ''
        part_search_option_str = ''
        for don in distributor_order_number:
            if len(mouser_part_number_str) > 0:
                mouser_part_number_str = mouser_part_number_str + "|" + don
                part_search_option_str = part_search_option_str + '|Exact'
            else:
                mouser_part_number_str = don
                part_search_option_str = "Exact"
        content = {"SearchByPartRequest": {"mouserPartNumber": mouser_part_number_str,
                                           "partSearchOptions": part_search_option_str}}
        response = requests.post(self.__build_request_url('search', 'partnumber'), json=content)
        return response

    def test(self):
        mouser_part_data = {'Availability': '27035 In Stock',
                            'DataSheetUrl': 'https://www.mouser.com/datasheet/2/256/DS18B20-370043.pdf',
                            'Description': 'Board Mount Temperature Sensors Programmable Resolution 1-Wire Digital Thermometer',
                            'FactoryStock': '0',
                            'ImagePath': 'https://www.mouser.com/images/mouserelectronics/images/A_TO_92_3_t.jpg',
                            'Category': 'Board Mount Temperature Sensors', 'LeadTime': '77 Days', 'LifecycleStatus': '',
                            'Manufacturer': 'Maxim Integrated', 'ManufacturerPartNumber': 'DS18B20+', 'Min': '1',
                            'Mult': '1', 'MouserPartNumber': '700-DS18B20+',
                            'ProductAttributes': [{'AttributeName': 'Packaging', 'AttributeValue': 'Tube'},
                                                  {'AttributeName': 'Standard Pack Qty', 'AttributeValue': '2000'}],
                            'PriceBreaks': [{'Quantity': 1, 'Price': '19,14 zł', 'Currency': 'PLN'},
                                            {'Quantity': 10, 'Price': '17,20 zł', 'Currency': 'PLN'},
                                            {'Quantity': 25, 'Price': '16,28 zł', 'Currency': 'PLN'},
                                            {'Quantity': 50, 'Price': '15,80 zł', 'Currency': 'PLN'}],
                            'AlternatePackagings': [{'APMfrPN': 'DS18B20+T&R'}],
                            'ProductDetailUrl': 'https://pl.mouser.com/ProductDetail/Maxim-Integrated/DS18B20%2b/?qs=7H2Jq%252ByxpJKegCKabDbglA%3D%3D',
                            'Reeling': False, 'ROHSStatus': 'RoHS Compliant', 'SuggestedReplacement': '',
                            'MultiSimBlue': 0, 'InfoMessages': [],
                            'ProductCompliance': [{'ComplianceName': 'TARIC', 'ComplianceValue': '8542399000'},
                                                  {'ComplianceName': 'CAHTS', 'ComplianceValue': '8542390000'},
                                                  {'ComplianceName': 'CNHTS', 'ComplianceValue': '8542399000'},
                                                  {'ComplianceName': 'USHTS', 'ComplianceValue': '8542390001'},
                                                  {'ComplianceName': 'JPHTS', 'ComplianceValue': '8542390990'},
                                                  {'ComplianceName': 'MXHTS', 'ComplianceValue': '85423999'},
                                                  {'ComplianceName': 'ECCN', 'ComplianceValue': 'EAR99'}]}
        print(self.__encode_part(mouser_part_data))


def main():
    mouser = Mouser()
    mouser.test()
    # print(mouser.find_component("700-DS18B20+").json())


if __name__ == "__main__":
    main()
