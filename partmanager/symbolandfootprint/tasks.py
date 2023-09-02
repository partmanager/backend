import logging
from celery import shared_task
from .models import Symbol
from .symbol_exporter.symbol_exporter_svg import SymbolExporterSVG


@shared_task
def generate_symbol_file(symbol: Symbol):
    if symbol.symbol is not None:
        svg_symbol = SymbolExporterSVG(symbol.name, symbol.symbol)
        svg_symbol.export_to_file('/static/symbolandfootprint/symbols/' + str(symbol.name) + ".svg")
        symbol.svg_file_generated = True
        symbol.save()
