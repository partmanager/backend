from django.db import models


class Symbol(models.Model):
    name = models.CharField(max_length=200, unique=True)
    symbol = models.JSONField(null=True)
    svg_file_generated = models.BooleanField(default=False)
    interactive_svg_file_generated = models.BooleanField(default=False)


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


