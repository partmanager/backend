from composite_field import CompositeField
from django.db import models
import json
import decimal


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)


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
    reel_diameter = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    reel_diameter_unit = models.CharField(max_length=1, choices=DIAMETER_UNIT, null=True, blank=True)
    reel_width = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    tape_w = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape width in mm.", blank=True, null=True)
    tape_t = models.DecimalField(max_digits=4, decimal_places=3, help_text="Tape thickness in mm",
                                 blank=True, null=True)
    tape_k = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape thickness with embossment in mm",
                                 blank=True, null=True)
    tape_e = models.DecimalField(max_digits=4, decimal_places=3,
                                 help_text="Distance between sprocket hole center and tape edge in mm",
                                 blank=True, null=True)
    tape_f = models.DecimalField(max_digits=4, decimal_places=2,
                                 help_text="Distance between sprocket hole center and component cavity center in mm",
                                 blank=True, null=True)
    tape_d = models.DecimalField(max_digits=4, decimal_places=3, help_text="Sprocket hole diameter in mm",
                                 blank=True, null=True)
    tape_d1 = models.DecimalField(max_digits=4, decimal_places=3, help_text="Component cavity hole diameter in mm",
                                  blank=True, null=True)
    tape_pin_1_quadrant = models.CharField(max_length=1, choices=PIN1_QUADRANT,
                                           help_text="Part pin 1 orientation on tape.",
                                           default='u')
    tape_so = models.DecimalField(max_digits=4, decimal_places=2, help_text="Sprocket holes distance in mm.",
                                  blank=True, null=True)
    tape_p0 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Sprocket holes pitch in mm.",
                                  blank=True, null=True)
    tape_p1 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape cavity pitch in mm",
                                  blank=True, null=True)
    tape_p2 = models.DecimalField(max_digits=4, decimal_places=2,
                                  help_text="Offset between cavity center and sprocket hole center in mm",
                                  blank=True, null=True)
    tape_a0 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape cavity dimension A0 in mm.",
                                  blank=True, null=True)
    tape_a1 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape cavity dimension A1 in mm.",
                                  blank=True, null=True)
    tape_b0 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape cavity dimension B0 in mm.",
                                  blank=True, null=True)
    tape_b1 = models.DecimalField(max_digits=4, decimal_places=2, help_text="Tape cavity dimension B1 in mm.",
                                  blank=True, null=True)

    class Proxy(CompositeField.Proxy):
        def to_json(self):
            return json.dumps(self.to_dict(), cls=Encoder)





