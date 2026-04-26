from django.db import models
from django.core.exceptions import FieldDoesNotExist  # NOQA
from .product import Product


class PartSeries(models.Model):
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


class Part(Product):
    device_marking_code = models.CharField(max_length=20, null=True, blank=True)
    symbol = models.ForeignKey('symbolandfootprint.Symbol', on_delete=models.PROTECT, blank=True, null=True)
    # footprints = models.ManyToManyField(Footprint)
    package = models.ForeignKey('packages.Package', on_delete=models.PROTECT, blank=True, null=True)

    fields_begin = {'MPN': 'manufacturer_part_number', 'OPN': 'manufacturer_order_number',
                    'Production Status': 'production_status', 'Description': 'description'}
    fields_end = {'Package': 'package', 'Marking Code': 'device_marking_code',
                  'Working temperature range': 'working_temperature_range',
                  'Storage conditions': 'storage_conditions', 'Manufacturer': 'manufacturer'}
    fields = {**fields_begin, **fields_end}

    class Meta:
        abstract = True


    def operating_temperature_range(self):
        if self.operating_conditions.temperature_min and self.operating_conditions.temperature_max:
            return "{}..{}\u2103".format(self.working_temperature_min, self.working_temperature_max)
        elif self.operating_conditions.temperature_max:
            return "max: {}\u2103".format(self.operating_conditions.temperature_max)
        elif self.operating_conditions.temperature_min:
            return "min: {}\u2103".format(self.operating_conditions.temperature_min)
        else:
            return ''

    @property
    def storage_temperature_range(self): # todo delete
        if self.storage_conditions.temperature_min and self.storage_conditions.temperature_max:
            return "{}..{}\u2103".format(self.storage_conditions.temperature_min, self.storage_conditions.temperature_max)
        elif self.storage_conditions.temperature_max:
            return "{max: {}\u2103".format(self.storage_temperature_max)
        elif self.storage_conditions.temperature_min:
            return "{min: {}\u2103".format(self.storage_temperature_min)
        else:
            return ''

    def get_package_display(self):
        return self.package.name if self.package else 'Unknown'

    @property
    def icon_image(self):
        if self.package:
            return self.package.image_icon()

    @property
    def distributor_pk_set_urlencoded(self): # todo delete
        pk_set = []
        for mon in self.manufacturer_order_number_set.all():
            for don in mon.distributorordernumber_set.all():
                pk_set.append(don.pk)
        return 'pk=' + '&pk='.join(str(s) for s in pk_set)

    def distributor_pk_set(self):
        pk_set = []
        for mon in self.manufacturer_order_number_set.all():
            for don in mon.distributorordernumber_set.all():
                pk_set.append(don.pk)
        return pk_set

    def get_package_display(self):
        if self.package:
            return "{}".format(self.package.name)
        return ""

    @staticmethod
    def part_type_from_str(connector_str):
        values = {'Aluminium Electrolytic Capacitor': 'CE', 'MLCC': 'MCC',
                  'Balun': 'BAL',
                  'Battery': 'BAT',
                  'Bridge Rectifier': 'BRG',
                  'Common Mode Choke': 'CMC',
                  'PTC Fuse': 'PFU',
                  'Relay': 'RLY',
                  'Resistor': 'R',
                  'Resistor Carbon Film': 'RCF',
                  'Resistor Thick Film': 'RTK',
                  'Resistor Thin Film': 'RTN',
                  'Resistor Metal Film': 'RMF',
                  'Resistor Array': 'RA',
                  'Connector': 'CON',
                  'Connector Bus': 'COB',
                  'Connector Pins': 'COP',
                  "Connector Terminal Block": 'COT',
                  "Connector FFC/FPC": 'COF',
                  "Connector IDC": "COI",
                  "Connector microSD Card": 'CO5',
                  'Connector Accessory': 'COA',
                  "Crystal": 'COS',
                  'Crystal Oscillator': 'CRO',
                  'Enclosure': 'E',
                  'Enclosure Accessory': 'EA',
                  'ESD Suppressor': 'ESD',
                  'Inductor': 'I',
                  'Ferrite Bead': 'FB',
                  'Fuse': 'FUS',
                  'Schottky Diode': 'DS',
                  'TVS': 'TVS',
                  'Small Signal Diode': 'D',
                  'Surge arrester': 'SAR',
                  'Transistor NPN': 'TBN',
                  'Transistor PNP': 'TBP',
                  'Transistor MOSFET N Dual Gate': 'MDN',
                  'Transistor MOSFET N': 'MON',
                  'Transistor MOSFET P': 'MOP',
                  'IC': 'IC',
                  'IC ADC': 'IAD',
                  'IC DAC': 'IDA',
                  'IC Opamp': 'IC',
                  'IC Comparator': 'ICO',
                  'IC Voltage Regulator': 'ICV',
                  'IC Voltage Reference': 'ICR',
                  'IC RF Amplifier': 'IRF',
                  'IC RF Synthesizer': 'IRS',
                  'IC LDO': "ICV",
                  'IC Voltage Regulator Switching': 'ICV',
                  'IC Level translator': 'ICL',
                  'IC Current Sense': 'ICC',
                  'IC MCU': 'IMC',
                  'IC Load Switch': 'ICS',
                  'IC Sensor': 'ICN',
                  'Module': 'M',
                  'Battery Holder': 'BH',
                  'Switch': 'S',
                  'LCD Display': 'DIS',
                  'LED': 'DLE',
                  'Lightpipe': 'LPI',
                  'Zener Diode': 'DZ',
                  'Varistor': 'VAR',
                  'PCB': 'PCB'}
        return values[connector_str]
