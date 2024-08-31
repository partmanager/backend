import logging
from celery import shared_task
from .models import Symbol
from django.conf import settings


@shared_task
def generate_symbol_file(symbol: Symbol):
    if symbol.symbol and symbol.name:
        base_path = settings.MEDIA_ROOT + "/symbols/svg/"
        for part in symbol.part_set.all():
            print("=======", part)


@shared_task
def generate_symbols():
    objects = Symbol.objects.filter(symbol__isnull=False)
    for symbol in objects:
        symbol.export_svg()
