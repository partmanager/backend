import re


def decode_tme_barcode(barcode: str):
    tme_regexpr = r"P([\w\.\-\/%]*) 1P([\w\.\-\\/)\(,]*) Q(\d*) (?:4L\w* )?K(\d*)/(\d*)"
    tme_regexpr_compiled = re.compile(tme_regexpr)
    matched = tme_regexpr_compiled.match(barcode)
    if matched:
        result = {'distributor': {'name': 'TME'},
                  'order_number': {'number': matched.group(4), 'position': matched.group(5)},
                  'invoice': None,
                  'manufacturer_order_number': matched.group(2),
                  'distributor_order_number': {'text': matched.group(1), 'don': None},
                  'quantity': matched.group(3),
                  'manufacturer': {}}
        return result
