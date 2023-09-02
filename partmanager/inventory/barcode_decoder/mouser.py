import re


def decode_mouser_barcode(barcode):
    mouser_regexpr = r"(>\[\)>|\[\)>\^)06\][Kk](\d*)\]14K(\d*)]1P([\w\.\-\, ]*)\][Qq](\d*)\]11K(\d*)](4LCN|4LHU|4LPH|4LDE)]1V([\w\/ ]*)(\^d)?"
    mouser_regexpr_compiled = re.compile(mouser_regexpr)
    matched = mouser_regexpr_compiled.match(barcode)
    if matched:
        result = {'distributor': {'name': 'Mouser'},
                  'order_number': {'number': matched.group(2), 'position': None},
                  'invoice': {'position': int(matched.group(3)), 'number': matched.group(6)},
                  'manufacturer_order_number': matched.group(4),
                  'distributor_order_number': {},
                  'quantity': float(matched.group(5)),
                  'manufacturer': {'name': matched.group(8)}}
        return result


