import decimal
from django.db import models
from django.core.exceptions import FieldDoesNotExist  # NOQA
from .choices import ProductionStatus, PART_TYPE
from .files import File
from .fields.operating_conditions import OperatingConditions
from .fields.storage_conditions import StorageConditions
from .to_string_conversions import decimal_ppm_to_str, decimal_celsius_to_str
from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import ArrayField


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


class PartSeries(models.Model):
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Part(PolymorphicModel):
    part_type = models.CharField(max_length=3, choices=PART_TYPE, default='UNK')
    generated = models.BooleanField(default=False)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT)
    MPN = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    series = models.ManyToManyField('PartSeries', blank=True)
    device_marking_code = models.CharField(max_length=20, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    comment = models.TextField(null=True, blank=True) # TODO remove
    product_url = models.URLField(null=True, blank=True) # in case of generic part calculated field pointing to part specs in frontend
    operating_conditions = OperatingConditions()
    storage_conditions = StorageConditions()
    files = models.ManyToManyField(File, blank=True)
    thumbnail = models.ImageField(max_length=250, upload_to='part_catalog/images/', blank=True, null=True)
    images = ArrayField(models.ImageField(max_length=250, upload_to='part_catalog/images/'), blank=True, null=True)

    # TODO fields that should be moved to different model
    symbol = models.ForeignKey('symbolandfootprint.Symbol', on_delete=models.PROTECT, blank=True, null=True)
    # footprints = models.ManyToManyField(Footprint)
    package = models.ForeignKey('packages.Package', on_delete=models.PROTECT, blank=True, null=True)

    # generic part fields
    generic = models.BooleanField(default=False)
    filters = models.JSONField(null=True, blank=True)
    MONs = models.ManyToManyField('partcatalog.ManufacturerOrderNumber', related_name="generics", blank=True) # when
    # generic is False this field is calculated. It contains references to ManufacturerOrderNumber model

    # calculated fields
    production_status = models.IntegerField(choices=ProductionStatus.choices, default=ProductionStatus.UNKNOWN) # calculated field


    fields_begin = {'MPN': 'manufacturer_part_number', 'OPN': 'manufacturer_order_number',
                    'Production Status': 'production_status', 'Description': 'description'}
    fields_end = {'Package': 'package', 'Marking Code': 'device_marking_code',
                  'Working temperature range': 'working_temperature_range',
                  'Storage conditions': 'storage_conditions', 'Manufacturer': 'manufacturer'}
    fields = {**fields_begin, **fields_end}

    class Meta:
        unique_together = ['manufacturer', 'MPN']
        ordering = ['manufacturer', 'MPN']
        index_together = [
            ["manufacturer", "MPN"],
        ]

    def save(self, *args, **kwargs):
        self.update_calculated_fields()
        super(Part, self).save(*args, **kwargs)

    def update_calculated_fields(self):
        self._update_production_status_field()
        self._update_MONs_field()

    def _update_production_status_field(self):
        self.production_status = ProductionStatus.OBSOLETE
        for mon in self.MONs.all():
            if mon.productionStatus != ProductionStatus.OBSOLETE:
                self.production_status = ProductionStatus.IN_PRODUCTION
                break

    def _update_MONs_field(self):
        if not self.generic:
            self.MONs.set(self.manufacturerordernumber_set.all())



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

    # def get_storage_conditions_display(self):
    #     return str(self.storage_conditions)

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

    # def get_part_group_name(self):
    #     part_type_dict = dict(Part.PART_TYPE)
    #     part_group_names = list(part_type_dict.keys())
    #     #print(part_group_names)
    #     for part_group_name in part_group_names:
    #         #print(part_type_dict[part_group_name])
    #         try:
    #             if dict(part_type_dict[part_group_name]):
    #                 part_group = self.get_part_type_group(part_group_name)
    #                 if self.part_type in part_group:
    #                     return part_group_name
    #         except:
    #             pass

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

    # @staticmethod
    # def get_part_type_group(part_group_name):
    #     part_type_group = dict(Part.PART_TYPE)
    #     if part_group_name == 'nongroup':
    #         nongroup = []
    #         for key in part_type_group:
    #             try:
    #                 dict(part_type_group[key])
    #             except:
    #                 nongroup.append(key)
    #         return nongroup
    #     else:
    #         return list(dict(part_type_group[part_group_name]).keys())
