import json
import logging

from celery import shared_task
from .models import Symbol, Footprint
from django.conf import settings
from packages.models.common import Package
from part_library_gen import footprint_generator
from part_library_gen.exporters.svg.footprint_exporter import export
from django.core.serializers.json import DjangoJSONEncoder


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


def generate_footprints():
    for package in Package.objects.all():
        footprint_data = {
            "generator": package.type,
            "data": package.to_part_lib_gen_obj()
        }
        generated_footprint, footprint_name = footprint_generator.generate(footprint_data)
        footprint, created = Footprint.objects.get_or_create(
            name=footprint_name,
            footprint=json.dumps(generated_footprint.to_dict(), cls=DjangoJSONEncoder),
            defaults={'package': package}
        )
        #footprint.save()
        base_path = settings.MEDIA_ROOT + '/' + "footprints/svg/"
        export(generated_footprint, base_path + footprint_name)

