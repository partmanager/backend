import decimal
from django.db import models
from django.core.exceptions import FieldDoesNotExist  # NOQA
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .files import File
from .fields.operating_conditions import OperatingConditions
from .fields.storage_conditions import StorageConditions
from .to_string_conversions import decimal_ppm_to_str, decimal_celsius_to_str
from symbolandfootprint.models import Footprint
from polymorphic.models import PolymorphicModel


def decimal_voltage_to_str(voltage):
    if voltage == decimal.Decimal('0'):
        return '0V'
    elif voltage >= 1:
        voltage_str = str(voltage)
        if '.' in voltage_str:
            return voltage_str.rstrip('0').rstrip('.') + 'V'
        else:
            return voltage_str + 'V'
    elif voltage >= decimal.Decimal('0.001'):
        return str(voltage * 1000).rstrip('0').rstrip('.') + 'mV'
    elif voltage >= decimal.Decimal('0.000001'):
        return str(voltage * 1000000).rstrip('0').rstrip('.') + 'uV'


def decimal_current_to_str(current):
    if current >= 1:
        return str(current).rstrip('0').rstrip('.') + 'A'
    elif current >= decimal.Decimal('0.001'):
        return str(current * 1000).rstrip('0').rstrip('.') + 'mA'
    elif current >= decimal.Decimal('0.000001'):
        return str(current * 1000000).rstrip('0').rstrip('.') + 'uA'
    elif current >= decimal.Decimal('0.000000001'):
        return str(current * 1000000000).rstrip('0').rstrip('.') + 'nA'


def decimal_to_str(value):
    value_str = str(value)
    if '.' in value_str:
        value_str = value_str.rstrip('0').rstrip('.')
    return value_str


def decimal_resistance_to_str(frequency):
    if frequency >= 1000000:
        return str(frequency / 1000000).rstrip('0').rstrip('.') + 'M\u2126'
    elif frequency >= 1000:
        return str(frequency / 1000).rstrip('0').rstrip('.') + 'k\u2126'
    elif frequency >= 1:
        value_str = str(frequency)
        if '.' in value_str:
            value_str = value_str.rstrip('0').rstrip('.')
        return value_str + '\u2126'
    elif frequency >= decimal.Decimal('0.001'):
        return str(frequency * 1000).rstrip('0').rstrip('.') + 'm\u2126'
    elif frequency >= decimal.Decimal('0.000001'):
        return str(frequency * 1000000).rstrip('0').rstrip('.') + 'u\u2126'


def decimal_impedance_to_str(impedance):
    return decimal_resistance_to_str(impedance)


class Part(PolymorphicModel):
    PART_TYPE = [
        ('Resistors', (
            ('GR', 'Generic Resistor'),
            ('R', 'Resistor'),
            ('RA', 'Resistor Array'),
            ('RCF', 'Resistor Carbon Film'),
            ('RTK', 'Resistor Thick Film'),
            ('RTN', 'Resistor Thin Film'),
            ('RMF', 'Resistor Metal Film'))
        ),
        ('Capacitors', (
            ('C', 'Capacitor'),
            ('CC', 'Ceramic Capacitor'),
            ('MCC', 'Multi Layer Ceramic Capacitor'),
            ('CE', 'Electrolitic Capacitor'),
            ('CP', 'Polymer Capacitor'),
            ('CT', 'Tantalum Capacitor'))
        ),
        ('I', 'Inductor'),
        ('FB', 'Ferrite Bead'),
        ('CMC', 'Common Mode Choke'),
        ('BAL', 'Balun'),
        ('Diodes', (
            ('BRG', 'Bridge Rectifier'),
            ('D', 'Small Signal Diode'),
            ('DS', 'Schottky Diode'),
            ('DLE', 'LED'),
            ('DZ', 'Zener Diode'))
         ),
        ('TVS', 'Transient Voltage Suppressor'),
        ('ESD', 'ESD Suppressor'),
        ('SAR', 'Surge Arrester'),
        ('Transistors', (
            ('T', 'Transistor'),
            ('TBN', 'Transistor NPN'),
            ('MON', 'Transistor MOS N'),
            ('MOP', 'Transistor MOS P'),
            ('TBP', 'Transistor PNP'))
        ),
        ('COS', 'Crystal'),
        ('CRO', 'Crystal Oscillator'),
        ('F', 'Fuse'),
        ('Integrated Circuits', (
            ('IC', 'Integrated Circuit'),
            ('ICV', 'Integrated Circuit Voltage Regulator'),
            ('ICR', 'Integrated Circuit Voltage Reference'),
            ('IRF', 'Integrated Circuit RF Amplifier'),
            ('IRS', 'Integrated Circuit RF Synthesizer'))
        ),
        ('Connectors', (
            ('CON', 'Connector'),
            ('COB', 'Connector Bus'),
            ('COT', "Connector Terminal Block"),
            ('COF', "Connector FFC/FPC"),
            ('CO5', "Connector microSD Card"),
            ('COI', 'Connector IDC'),
            ('COA', 'Connector Accessory'))
        ),
        ('DIS', 'LCD Display'),
        ('LDI', 'LED Display'),
        ('LOI', 'OLED Display'),
        ('LPI', 'Lightpipe'),
        ('B', 'Battery'),
        ('Materials', (
            ('MSW', 'Solder Wire'),
            ('MSP', 'Solder Paste'))
         ),
        ('Mechanical', (
            ('BH', 'Battery Holder'),
            ('E', 'Enclosure'),
            ('EA', 'Enclosure Accessory'))
        ),
        ('M', 'Module'),
        ('S', 'Switch'),
        ('VAR', 'Varistor'),
        ('PCB', 'PCB')
    ]
    PRODUCTION_STATUS = (
        ('PRE', 'Preview'),
        ('ACT', 'In Production'),
        ('NRD', 'Not Recommended for New Design'),
        ('LTB', 'Last Time Buy'),
        ('OBS', 'Obsolete'),
        ('UNK', 'Unknown')
    )

    part_type = models.CharField(max_length=3, choices=PART_TYPE, default='UNK')
    generated = models.BooleanField(default=False)
    manufacturer_part_number = models.CharField(max_length=200)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    series = models.CharField(max_length=100, null=True, blank=True)
    series_description = models.CharField(max_length=250, null=True, blank=True)
    # package = models.ForeignKey('packages.Package', on_delete=models.PROTECT, blank=True, null=True)
    package_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    package_object_id = models.PositiveIntegerField(blank=True, null=True)
    package = GenericForeignKey('package_content_type', 'package_object_id')
    description = models.CharField(max_length=300, blank=True)
    production_status = models.CharField(max_length=3, choices=PRODUCTION_STATUS, default='UNK')
    device_marking_code = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(max_length=200, null=True, blank=True)
    comment = models.TextField(max_length=2000, null=True, blank=True)
    product_url = models.URLField(null=True, blank=True)
    #working_temperature_min = models.IntegerField(null=True, blank=True)
    #working_temperature_max = models.IntegerField(null=True, blank=True)
    #storage_temperature_min = models.IntegerField(null=True, blank=True)
    #storage_temperature_max = models.IntegerField(null=True, blank=True)
    operating_conditions = OperatingConditions()
    storage_conditions = StorageConditions()
    symbol = models.ForeignKey('symbolandfootprint.Symbol', on_delete=models.PROTECT, blank=True, null=True)
    #footprints = models.ManyToManyField(Footprint)
    files = models.ManyToManyField(File)

    fields_begin = {'MPN': 'manufacturer_part_number', 'OPN': 'manufacturer_order_number',
                    'Production Status': 'production_status', 'Description': 'description'}
    fields_end = {'Package': 'package', 'Marking Code': 'device_marking_code',
                  'Working temperature range': 'working_temperature_range',
                  'Storage conditions': 'storage_conditions', 'Manufacturer': 'manufacturer'}
    fields = {**fields_begin, **fields_end}

    class Meta:
        unique_together = ['manufacturer', 'manufacturer_part_number']
        ordering = ['manufacturer_part_number']
        #indexes = ['manufacturer_part_number']
        index_together = [
            ["manufacturer", "manufacturer_part_number"],
        ]

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

    def get_storage_conditions_display(self):
        return str(self.storage_conditions)

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

    def get_part_group_name(self):
        part_type_dict = dict(Part.PART_TYPE)
        part_group_names = list(part_type_dict.keys())
        #print(part_group_names)
        for part_group_name in part_group_names:
            #print(part_type_dict[part_group_name])
            try:
                if dict(part_type_dict[part_group_name]):
                    part_group = self.get_part_type_group(part_group_name)
                    if self.part_type in part_group:
                        return part_group_name
            except:
                pass

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
                  'IC Voltage Regulator': 'ICV',
                  'IC Voltage Reference': 'ICR',
                  'IC RF Amplifier': 'IRF',
                  'IC RF Synthesizer': 'IRS',
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

    @staticmethod
    def get_part_type_group(part_group_name):
        part_type_group = dict(Part.PART_TYPE)
        if part_group_name == 'nongroup':
            nongroup = []
            for key in part_type_group:
                try:
                    dict(part_type_group[key])
                except:
                    nongroup.append(key)
            return nongroup
        else:
            return list(dict(part_type_group[part_group_name]).keys())

    def get_on_stock_quantity(self):
        quantity = 0
        average_price = 0
        storage_locations = ""
        storage_locations_array = []
        for mon in self.manufacturer_order_number_set.all():
            for inventory_position in mon.inventoryposition_set.all():
                storage_dict = {'location': inventory_position.storage_location.location,
                                'quantity': inventory_position.stock,
                                'price': '-',
                                'invoice': '-'}
                quantity = quantity + inventory_position.stock
                if len(storage_locations) > 0:
                    storage_locations = storage_locations + ', ' + inventory_position.storage_location.location
                else:
                    storage_locations = inventory_position.storage_location.location
                if inventory_position.invoice:
                    average_price = average_price + inventory_position.stock * inventory_position.invoice.get_price_per_unit()
                    storage_dict['price'] = inventory_position.invoice.get_price_per_unit_display()
                    storage_dict['invoice'] = inventory_position.invoice.get_invoice_number_display()
                storage_locations_array.append(storage_dict)

        if average_price != 0:
            average_price = average_price / quantity
        return {"quantity": quantity, "storage_locations": storage_locations, 'average_price': average_price,
                'locations_array': storage_locations_array}

    def get_files_array(self):
        files = []
        for file in self.files.all():
            files.append(file.to_ajax_response())
        return files

    # def to_view_ajax_response(self):
    #     id_field = self.pk
    #     result = [{"id": id_field,
    #                "pid": 0,
    #                'part_type': self.get_part_type_display(),
    #                "manufacturer_part_number": self.manufacturer_part_number,
    #                "description": self.description,
    #                "production_status": dict(self.PRODUCTION_STATUS)[self.production_status],
    #                "package": self.package.name if self.package else 'Unknown',
    #                "working_temperature_range": self.working_temperature_range,
    #                "storage_conditions": str(self.storage_conditions),
    #                "manufacturer": self.manufacturer.name,
    #                "product_url": self.product_url,
    #                "files": self.get_files_array()
    #                }]
    #     if self.manufacturer_order_number_set:
    #         mons = []
    #         for manufacturer_order_number in self.manufacturer_order_number_set.all():
    #             mons.append({'id': manufacturer_order_number.id,
    #                          "manufacturer_order_number": manufacturer_order_number.manufacturer_order_number,
    #                          "production_status": self.production_status})
    #     #         order = {"id": -id_field,
    #     #                  "pid": id_field,
    #     #                  "manufacturer_part_number": self.manufacturer_part_number,
    #     #                  "manufacturer_order_number": package.manufacturer_order_number,
    #     #                  "production_status": dict(self.PRODUCTION_STATUS)[self.production_status],
    #     #                  "description": package.description}
    #     #         result.append(order)
    #         result[0]['manufacturer_order_number'] = mons
    #
    #     return result

    # def to_ajax_response(self):
    #     id_field = self.pk
    #     result = [{"id": id_field,
    #                "pid": 0,
    #                'part_type': self.get_part_type_display(),
    #                "manufacturer_part_number": self.manufacturer_part_number,
    #                "description": self.description,
    #                "production_status": dict(self.PRODUCTION_STATUS)[self.production_status],
    #                "package": self.package.name if self.package else 'Unknown',
    #                "working_temperature_range": self.working_temperature_range,
    #                "storage_temperature_range": self.storage_temperature_range,
    #                "manufacturer": self.manufacturer.name,
    #                "product_url": self.product_url
    #                }]
    #     return result
