from ..models.generic_part import GenericPart
from ..models.to_string_conversions import decimal_resistance_to_str
from manufacturers.models import get_manufacturer_by_name
from decimal import Decimal

def generate_generic_resistors():
    print('Generating generic resistors...')
    series_e24 = [
        Decimal('1.0'),
        Decimal('1.1'),
        Decimal('1.2'),
        Decimal('1.3'),
        Decimal('1.5'),
        Decimal('1.6'),
        Decimal('1.8'),
        Decimal('2.0'),
        Decimal('2.2'),
        Decimal('2.4'),
        Decimal('2.7'),
        Decimal('3.0'),
        Decimal('3.3'),
        Decimal('3.6'),
        Decimal('3.9'),
        Decimal('4.3'),
        Decimal('4.7'),
        Decimal('5.1'),
        Decimal('5.6'),
        Decimal('6.2'),
        Decimal('6.8'),
        Decimal('7.5'),
        Decimal('8.2'),
        Decimal('9.1')
    ]
    multi = [1, 10, 100, 1000, 10000]
    for n in multi:
        for series_resistance in series_e24:
            resistance = series_resistance * n
            resistance_str = decimal_resistance_to_str(resistance)
            resistor = GenericPart(
                part_type='R',
                generated = True,
                manufacturer = get_manufacturer_by_name('Unknown'),
                manufacturer_part_number=f'R_{resistance_str}_5%_0402',
                description= f"Generic Resistor {resistance_str} 5% 0402",
                comment=f"Generic Resistor {resistance_str} 5% 0402",
                filters={
                    'resistance': {'value': int(resistance)},
                    'tolerance': {'value': 1},
                    'package': {'value': "0402"}
                }
            )

            try:
                resistor.save()
            except Exception as ex:
                print(ex)