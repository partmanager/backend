from django.db import models


class BatteryType(models.IntegerChoices):
    CR2030 = 1
    CR2032 = 2
    R6 = 3
    CR14250 = 4

    @staticmethod
    def from_string(type_str):
        values = {'CR2030': 1, "CR2032": 2, 'R6': 3, 'AA, R6': 3, 'CR14250': 4}
        return values[type_str]


class BatteryClassification(models.IntegerChoices):
    ALKALINE = 1
    LITHIUM = 2

    @staticmethod
    def from_string(type_str):
        values = {'Alkaline': 1, 'Lithium': 2}
        return values[type_str]


class MaterialType(models.IntegerChoices):
    SOLDER_PASTE = 1

    @staticmethod
    def from_string(type_str):
        values = {'Solder Paste': 1}
        return values[type_str]


class MSLevel(models.IntegerChoices):
    MSL_1 = 1
    MSL_2 = 2
    MSL_2a = 22
    MSL_3 = 3
    MSL_4 = 4
    MSL_5 = 5
    MSL_5a = 52
    MSL_6 = 6

    @staticmethod
    def from_string(type_str):
        values = {'MSL-1 UNLIM': 1,
                  'MSL-2 1-YEAR': 2,
                  'MSL-2A 4-WEEKS': 22,
                  'MSL-3 168-HOURS': 3,
                  'MSL-4 72-HOURS': 4,
                  'MSL-5 48-HOURS': 5,
                  'MSL-5A 24-HOURS': 52,
                  'MSL-6 TOL': 6}
        if type_str in values:
            return values[type_str]
        else:
            raise ValueError(f"Invalid MSL level: {type_str}")


class ProductionStatus(models.IntegerChoices):
    UNKNOWN = 0
    PREVIEW = 1
    IN_PRODUCTION = 2
    NRD = 22 # Not Recommended for New Design
    LTB = 3 # Last Time Buy
    OBSOLETE = 4


    @staticmethod
    def from_string(type_str):
        values = {
            'Unknown': 0,
            'Preview': 1,
            'Production': 2,
            'NRD': 3,
            'LTB': 4,
            'Obsolete': 5
        }
        if type_str in values:
            return values[type_str]
        else:
            raise ValueError(f"Invalid Production status: {type_str}")


class ToleranceType(models.IntegerChoices):
    RELATIVE = 1
    ABSOLUTE = 2
    RELATIVE_PPM = 3

    @staticmethod
    def from_string(type_str):
        values = {'relative': 1, 'absolute': 2, 'ppm': 3}
        return values[type_str]


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
            ('ICL', 'IC Level translator'),
            ('ICC', 'IC Current Sense'),
            ('ICO', 'IC Comparator'),
            ('IMC', 'IC MCU'),
            ('IDA', 'IC DAC'),
            ('IAD', 'IC ADC'),
            ('ICN', 'IC Sensor'),
            ('ICS', 'IC Load Switch'),
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