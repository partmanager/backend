from django.db import models
from django.utils.timezone import now
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from manufacturers.models import get_manufacturer_by_name
from .connector.distributorApiConnector import get_distributor_api_connector
from partmanager.choices import MerchandiseType, QuantityUnit


class Distributor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website_url = models.URLField(max_length=200, null=True, blank=True)
    connector_data = models.JSONField(null=True, blank=True)
    # distributorordernumber_set -> reverse key form DistributorOrderNumber model
    # distributormanufacturer_set -> reverse key form DistributorManufacturer model

    class Meta:
        ordering = ['name']

    @staticmethod
    def get_by_name(name):
        try:
            return Distributor.objects.get(name=name)
        except Distributor.DoesNotExist:
            return None

    def part_count(self):
        return len(self.distributorordernumber_set.all())

    def part_without_mon_count(self):
        return self.distributorordernumber_set.filter(manufacturer_order_number__isnull=True).count()

    def __str__(self):
        return "{}".format(self.name)

    def convert_manufacturer_name(self, distributor_manufacturer_name):
        if distributor_manufacturer_name is not None:
            try:
                return self.distributormanufacturer_set.get(manufacturer_name_text=distributor_manufacturer_name)
            except DistributorManufacturer.DoesNotExist:
                return distributor_manufacturer_name

    def get_order_number(self, distributor_order_number):
        try:
            return self.distributorordernumber_set.get(distributor_order_number_text=distributor_order_number)
        except DistributorOrderNumber.DoesNotExist:
            return None

    def request_order_numbers(self, distributor_order_number_set):
        distributor_connector = self.__get_distributor_connector()
        if distributor_connector:
            if 'DELIVERY_AUTO' in distributor_order_number_set:
                distributor_order_number_set.remove('DELIVERY_AUTO')
            if len(distributor_order_number_set) > 0:
                print("Requested components ----------------------------")
                print(distributor_order_number_set)
                print("-------------------------------------------------")
                components = distributor_connector.get_component(list(distributor_order_number_set))
                print("Got response -------------------------------------", components)
                print("-------------------------------------------------")
                response = []
                for distributor_order_number in distributor_order_number_set:
                    found = 0
                    for component in components:
                        if distributor_order_number == component['Distributor Order Number']:
                            found = found + 1
                            if found == 1:
                                manufacturer = get_manufacturer_by_name(
                                    self.convert_manufacturer_name(component['Manufacturer']))
                                mon = ManufacturerOrderNumber.objects.filter(
                                    manufacturer_order_number=component['Manufacturer Part Number'],
                                    manufacturer=manufacturer)
                                don = DistributorOrderNumber(distributor=self,
                                                             distributor_order_number_text=distributor_order_number,
                                                             manufacturer_name_text=component['Manufacturer'],
                                                             manufacturer_order_number_text=component[
                                                                 'Manufacturer Part Number'],
                                                             manufacturer_order_number=mon[0] if len(
                                                                 mon) == 1 else None,
                                                             part_url=component['DistributorComponentWebPage'])
                                don.save()
                                print("DON:", don, "MON:", mon)
                                response.append({distributor_order_number: mon})
                            else:
                                print("-----------------------Error------------------")
                return response

    def update_distributor_order_numbers(self, category):
        distributor_connector = self.__get_distributor_connector()
        if distributor_connector:
            don_list = distributor_connector.get_components_don_from_category(category)
            components_list = distributor_connector.get_component(don_list)
            for component in components_list:
                defaults = {
                    'manufacturer_name_text': component['Manufacturer'],
                    'manufacturer_order_number_text': component['Manufacturer Part Number'],
                    'part_url': component['DistributorComponentWebPage']
                }
                DistributorOrderNumber.objects.update_or_create(distributor=self,
                                                                distributor_order_number_text=component[
                                                                    'Distributor Order Number'],
                                                                defaults=defaults)

    def request_stock_and_price(self, distributor_order_number_model_set):
        don_set = []
        for don in distributor_order_number_model_set:
            assert don.distributor == self
            don_set.append(don.distributor_order_number_text)
        if don_set:
            distributor_connector = self.__get_distributor_connector()
            stock_and_price = distributor_connector.get_stock_and_prices(don_set)
            return self.update_stock_and_price(stock_and_price)

    def get_stock_and_price(self, distributor_order_number_model_set):
        '''
        :return: array of dictionary's with format:
        {'distributor': {'name': '', 'url': ''},
         'distributorOrderNumber': {'don': '', 'url': ''},
         'manufacturerOrderNumber': '',
         'updateTime': '',
         'status': '',
         'stockCount': {'quantity': <>, 'unit': <'pcs', 'm', 'kg', 'l'>},
         'prices': {'quantity': <float/decimal/int>, 'unitPrice': <float/decimal>}
         }
        '''
        stock_and_price = []
        for don in distributor_order_number_model_set:
            assert don.distributor == self
            stock_and_price.append(don.get_stock_and_price())
        return stock_and_price

    def update_stock_and_price(self, stock_and_price):
        result = []
        for sap in stock_and_price:
            print("---------------------")
            print(sap)
            don = self.distributorordernumber_set.get(distributor_order_number_text=sap['distributorOrderNumber'])
            don.update_stock_and_price(sap)
            don.save()
            result.append(don.get_stock_and_price())
        return result

    def __get_distributor_connector(self):
        return get_distributor_api_connector(self.name)

    def to_dict(self):
        distributor_dict = {'name': self.name,
                            'website': self.website_url,
                            'connector_data': self.connector_data,
                            'manufacturer_name_translation': [],
                            'distributor_order_numbers': []}
        for mon_name in self.distributormanufacturer_set.all():
            distributor_dict['manufacturer_name_translation'].append(mon_name.to_dict())
        for don in self.distributorordernumber_set.all():
            distributor_dict['distributor_order_numbers'].append(don.to_dict())
        return distributor_dict


class DistributorOrderNumber(models.Model):
    """
    Distributor order number can point to:
        - part by 'manufacturer_order_number' field
        - service by 'service' field, service is in example shipping
    """
    distributor = models.ForeignKey('Distributor', on_delete=models.CASCADE)
    don = models.CharField(max_length=200, verbose_name="Distributor specific order number")
    mon = models.CharField(max_length=200,
                           null=True,
                           blank=True,
                           verbose_name="Distributor specific manufacturer order number")
    manufacturer_name = models.CharField(max_length=200,
                                         null=True,
                                         blank=True,
                                         verbose_name="Distributor specific manufacturer name")
    manufacturer_order_number = models.ForeignKey('partcatalog.ManufacturerOrderNumber',
                                                  on_delete=models.PROTECT,
                                                  null=True,
                                                  blank=True)
    part_url = models.URLField(max_length=500, null=True, blank=True)
    type = models.IntegerField(choices=MerchandiseType.choices, default=MerchandiseType.PART)

    stock = models.FloatField(null=True, blank=True)
    stock_unit = models.IntegerField(choices=QuantityUnit.choices, default=QuantityUnit.PCS)
    update_time = models.DateTimeField(null=True, blank=True)
    price_levels = models.JSONField(null=True, blank=True)
    # distributorstock_set reverse key with stock history

    class Meta:
        unique_together = ["distributor", "don"]
        ordering = ['distributor', 'manufacturer_name', 'don', 'mon']

    def get_stock_and_price(self):
        '''
        :return: array of dictionary's with format:
                {'distributor': {'name': '', 'url': ''},
                 'distributorOrderNumber': {'don': '', 'url': ''},
                 'manufacturerOrderNumber': '',
                 'updateTime': '',
                 'status': '',
                 'stockCount': {'quantity': <>, 'unit': <'pcs', 'm', 'kg', 'l'>},
                 'prices': {'quantity': <float/decimal/int>, 'unitPrice': <float/decimal>}
                 }
        '''
        distributor_stock = self.distributorstock_set.first()
        return {'id': self.pk,
                'distributor': {'name': self.distributor.name,
                                'url': self.distributor.website_url,
                                'id': self.distributor.pk},
                'distributorOrderNumber': {'don': self.don,
                                           'url': self.part_url},
                'manufacturerOrderNumber': str(
                    self.manufacturer_order_number) if self.manufacturer_order_number else '',
                'updateTime': distributor_stock.update_time,
                'status': '',
                'stockCount': {'quantity': distributor_stock.stock, 'unit': 'pcs'},
                'prices': distributor_stock.price_levels}

    def update_stock_and_price(self, stock_and_price):
        processed_price_list = []
        for price in stock_and_price['priceList']:
            price['price'] = float(price['price'])
            processed_price_list.append(price)
        self.update_time = now()
        self.stock = stock_and_price['stockCount']
        self.price_levels = processed_price_list

    def update_manufacturer_order_number(self):
        if self.manufacturer_order_number is None:
            manufacturer = get_manufacturer_by_name(
                self.distributor.convert_manufacturer_name(self.manufacturer_name))
            order_number = self.mon if self.mon else self.don
            mon = ManufacturerOrderNumber.objects.filter(
                manufacturer_order_number__iexact=order_number, manufacturer=manufacturer)
            print("Trying to assign part to DON:", self.don, "MON:",
                  self.mon, "Found Manufacturer:", manufacturer, "Found MON:", mon)
            if len(mon) == 1:
                self.manufacturer_order_number = mon[0]
                return mon[0]
            elif len(mon) > 1:
                print("Distributor order number, found more than one MON:", mon)

    def __str__(self):
        part_or_service = self.manufacturer_order_number.manufacturer_order_number if self.manufacturer_order_number else self.service.name if self.service else ''
        return "{}, {}, {} -> {}{}".format(self.distributor.name, self.manufacturer_name,
                                           self.don, self.mon, " --> " + part_or_service)

    def to_dict(self):
        don_dict = {'distributor_order_number': self.don,
                    'manufacturer_order_number': self.mon,
                    'manufacturer_name': self.manufacturer_name,
                    'part_url': self.part_url}
        return don_dict


class DistributorManufacturer(models.Model):
    distributor = models.ForeignKey('Distributor', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    manufacturer_name_text = models.CharField(max_length=200)

    class Meta:
        unique_together = ["distributor", "manufacturer_name_text"]
        ordering = ['distributor', 'manufacturer_name_text']

    def __str__(self):
        return "{}, {} -> {}".format(self.distributor.name, self.manufacturer_name_text, self.manufacturer.name)

    def to_dict(self):
        don_manufacturer_dict = {'distributor_manufacturer_name': self.manufacturer_name_text,
                                 'manufacturer_name': self.manufacturer.name}
        return don_manufacturer_dict


class DistributorStock(models.Model):
    don = models.ForeignKey('DistributorOrderNumber', on_delete=models.CASCADE)
    stock = models.FloatField(null=True, blank=True)
    stock_unit = models.IntegerField(choices=QuantityUnit.choices, default=QuantityUnit.PCS)
    update_time = models.DateTimeField(null=True, blank=True)
    price_levels = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ["don", "update_time"]
        ordering = ['don', '-update_time']
