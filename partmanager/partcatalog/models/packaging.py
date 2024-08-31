from composite_field import CompositeField
from django.db import models
import json
import decimal


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)


class Packaging(CompositeField):
    TYPE = (
        ('t', 'Tape/Reel'),
        ('p', 'Paper Tape / Reel'),
        ('e', 'Embossed Tape / Reel'),
        ('b', 'Bag'),
        ('u', 'Unknown')
    )

    DIAMETER_UNIT = (
        ('m', 'mm'),
        ('i', 'inch')
    )

    PIN1_QUADRANT = (
        ('1', 'Q1'),
        ('2', 'Q2'),
        ('3', 'Q3'),
        ('4', 'Q4')
    )

    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=40, choices=TYPE, default='u')
    quantity = models.IntegerField(blank=True, null=True)
    packaging_data = models.JSONField(null=True, blank=True)

    class Proxy(CompositeField.Proxy):
        def to_json(self):
            return json.dumps(self.to_dict(), cls=Encoder)





