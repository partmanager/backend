
class DistributorConnectorBase:
    def __init__(self, distributor_name, max_part_count_per_request):
        self.name = distributor_name
        self.max_part_count_per_request = max_part_count_per_request
        self.require_on_stock = True

    def get_component(self, distributor_order_number_set):
        chunked_list = self.get_chunked_list(distributor_order_number_set)
        components_list = []
        for chunk in chunked_list:
            components_list = components_list + self.get_component_impl(chunk)
        return components_list

    def get_component_impl(self, distributor_order_number_set):
        """
        :param distributor_order_number_set: set of distributor specific order number as string
        :return: array of dictionary
        """
        raise RuntimeError("Unimplemented")

    def get_stock_and_prices(self, distributor_order_number_set):
        """
        :param distributor_order_number_set: set of distributor specific order number as string
        :return: array of dictionary, ie:
            {'distributorOrderNumber': '0402B332K500CT',
             'stockCount': 100,
             'priceList': [
                {'amount': 100, 'price': 0.03789, 'currency': 'PLN', 'vatRate': 23, 'priceType': 'NET'},
                {'amount': 1000, 'price': 0.01396, 'currency': 'PLN', 'vatRate': 23, 'priceType': 'NET'}]
            }
        """
        raise RuntimeError("Unimplemented")

    def get_components_don_from_category(self, category):
        """
        :param category: category name as string
        :return: array of distributor order number, ie:
           ['TL431', 'LM358']
        """
        raise RuntimeError("Unimplemented")

    def find_component(self, manufacturer_part_number):
        """
        :param manufacturer_part_number: Manufacturer Part Number as string
        :return: array of components
        """
        raise RuntimeError("Unimplemented")

    def find_capacitor_by_parameters(self, capacitor):
        """
        :param capacitor: dictionary with fields:
                'Capacitance': Decimal in Farads,
                'Case': string
                'Voltage': int in Volts
                'Dielectric Type': string ie.: X7R, NP0 etc.
        :return:
        """
        raise RuntimeError("Unimplemented")

    def find_resistor_by_parameters(self, resistor):
        """
        :param resistor: dictionary with fields:
                'Resistance': Decimal in Ohms,
                'Case': string
                'Tolerance': percent as integer
        :return:
        """
        raise RuntimeError("Unimplemented")

    def get_chunked_list(self, symbol_list):
        symbol_list_chunk = []
        for i in range(0, len(symbol_list), self.max_part_count_per_request):
            symbol_list_chunk.append(symbol_list[i:i + self.max_part_count_per_request])
        return symbol_list_chunk