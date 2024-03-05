from .part import Part
from django.db import models
from django.utils.translation import gettext_lazy as _
from .fields.capacitance import Capacitance
from .fields.max_current import MaxCurrentAtTempAtFreq
from .fields.max_voltage import MaxVoltageAtTemp


class Capacitor(Part):
    CAPACITANCE_SUFIX = (
        ('pF', 'pF'),
        ('uF', 'uF'),
        ('mF', 'mF'),
        ('-F', 'F'),
        ('kF', 'kF'),
        ('MF', 'MF'),
        ('GF', 'GF'),
        ('TF', 'TF'),
    )

    # CAPACITOR_TYPE = (
    #     ('Ceramic Capacitor', 'Ceramic Capacitor'),
    #     ('Film Capacitor', 'Film Capacitor'),
    #     ('Aluminium Electrolytic Capacitor', 'Aluminium Electrolytic Capacitor'),
    #     ('Tantalum Electrolytic Capacitor', 'Tantalum Electrolytic Capacitor'),
    #     ('Niobium Electrolytic Capacitor', 'Niobium Electrolytic Capacitor'),
    #     ('MLCC', 'MLCC')
    # )

    class DielectricType(models.TextChoices):
        C0G = 'C0G'
        NP0 = 'NP0'
        X5R = 'X5R'
        X5S = 'X5S'
        X6T = 'X6T'
        X7R = 'X7R'
        X7S = 'X7S'
        X7T = 'X7T'
        X7U = 'X7U'
        Y5V = 'Y5V'

        @staticmethod
        def from_str(dielectric_str):
            values = {'B': 'B', 'R': 'R',
                      'CJ': 'CJ', 'CK': 'CK', 'SL': 'SL', 'CH': 'CH', 'UJ': 'UJ',
                      'C0G': 'C0G', 'C0H': 'C0H', 'CGJ': 'CGJ', 'NP0': 'NP0', 'X5R': 'X5R', 'X5S': 'X5S', 'X6S': 'X6S',
                      'X6T': 'X6T',
                      'X7R': 'X7R',
                      'X7S': 'X7S', 'X7T': 'X7T', 'X7U': 'X7U', 'Y5V': 'Y5V', 'U2J': 'U2J', 'U2K': 'U2K', 'X8G': 'X8G',
                      'X8L': 'X8L',
                      'Aluminium Oxide': 'AlO'}
            return values[dielectric_str]

    class ToleranceType(models.TextChoices):
        RELATIVE = '%', _('Relative')
        ABSOLUTE = 'pF', _('Absolute')

        @staticmethod
        def from_str(tolerance_str):
            values = {'Relative': '%', 'Absolute': 'pF'}
            return values[tolerance_str]

    part_type_subset = list(dict(dict(Part.PART_TYPE)['Capacitors']).keys())
    capacitance = Capacitance()
    voltage = MaxVoltageAtTemp()
    endurance = models.IntegerField(null=True, blank=True)  # for electrolytic capacitor
    rated_ripple_current = MaxCurrentAtTempAtFreq()  # for electrolytic capacitor
    dissipation_factor = models.DecimalField(max_digits=3, decimal_places=2, null=True,
                                             blank=True)  # for electrolytic capacitor
    dielectric_type = models.CharField(max_length=3, choices=DielectricType.choices, blank=True)

    fields = {**Part.fields_begin,
              'Capacitance': 'capacitance', 'Voltage': 'voltage', 'Tolerance': 'tolerance',
              'Dielectric Type': 'dielectric_type', 'Capacitor Type': 'capacitor_type',
              **Part.fields_end}

    def get_part_type_short_display(self):
        part_type_to_short_name = {'C': 'Capacitor', 'CC': 'Capacitor Ceramic', 'MCC': 'Capacitor MLCC',
                                   'CE': 'Capacitor Electrolitic', 'CP': 'Capacitor Polymer',
                                   'CT': 'Capacitor Tantalum'}
        return part_type_to_short_name[self.part_type]

    def generate_description(self):
        try:
            description = "{} {}, {}, {}, {}".format(self.get_part_type_short_display(),
                                                     self.capacitance,
                                                     self.voltage,
                                                     self.dielectric_type,
                                                     self.working_temperature_range)
            if self.package:
                description += ' ' + self.package.name
            return description
        except TypeError as e:
            print(self.manufacturer_part_number)
            print(self.get_part_type_short_display())
            print(self.capacitance)
            print(self.voltage)
            print(self.dielectric_type)
            print(self.working_temperature_range)

    class Meta:
        ordering = ['capacitance_typ', 'voltage_max', 'capacitance_relative_tolerance']

    def __str__(self):
        return '{} {}'.format(self.manufacturer.name, self.manufacturer_part_number)

    def get_capacitor_type_display(self):
        return self.get_part_type_short_display()

    def get_capacitance_display(self):
        return self.capacitance.get_capacitance_display()

    def get_tolerance_display(self):
        return self.capacitance.get_tolerance_display()

    def get_voltage_display(self):
        return str(self.voltage)
