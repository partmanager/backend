from django.contrib.postgres.fields import ArrayField
from django.db import models
from part_library_gen import symbol_generator
from django.conf import settings


class Symbol(models.Model):
    name = models.CharField(max_length=200, unique=True)
    symbol = models.JSONField(null=True, unique=True)
    pinmap = models.JSONField(null=True)
    generator_name = models.CharField(max_length=30, null=True, blank=True)
    generator_data = models.JSONField(null=True)
    svg_files = ArrayField(models.CharField(max_length=500), null=True, blank=True, default=list)
    svg_file_generated = models.BooleanField(default=False)
    interactive_svg_file_generated = models.BooleanField(default=False)

    def export_svg(self):
        base_path = settings.MEDIA_ROOT + '/' + "symbols/svg/"
        svg_files = []
        for part in self.part_set.all():
            symbol_data = {
                'designator': "*",
                'manufacturer': part.manufacturer.name,
                'part': part.manufacturer_part_number,
                'pins': self.pinmap,
                'symbol_generator': {self.generator_name: self.generator_data}
            }
            generated = symbol_generator.generate(symbol_data)
            if generated:
                symbol, symbol_name = generated[0]
                filename = f"{part.manufacturer.name.replace(' ', '_').lower()}_{part.manufacturer_part_number.replace('#', '')}{self.name}"
                symbol_generator.svg_exporter(symbol, base_path + filename)
                if len(symbol.parts) > 1:
                    svg_files = []
                    for i in range(0, len(symbol.parts)):
                         svg_files.append(f"{self.name}_{i}.svg")
                else:
                    svg_files = [f"{self.name}.svg"]
        self.svg_files = svg_files
        self.save()


class Footprint(models.Model):
    name = models.CharField(max_length=200, unique=True)


def get_symbol_by_name(symbol_name):
    symbols = Symbol.objects.filter(name=symbol_name)
    if len(symbols) == 1:
        return symbols[0]


def get_or_create_symbol(symbol_name):
    if len(symbol_name):
        symbols = Symbol.objects.filter(name=symbol_name)
        if len(symbols) > 0:
            assert len(symbols) == 1
            return symbols[0]
        else:
            new_symbol = Symbol(name=symbol_name)
            new_symbol.save()
            return new_symbol


