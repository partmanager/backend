import logging
from django.conf import settings
from pathlib import Path

from partsdb_tools.components.Part import Part
from manufacturers.models import get_or_create_manufacturer_by_name
from partcatalog.models.electronics_parts.triac import Triac
from partcatalog.models.part import Part as Part_db
from partcatalog.models.files import File, FileVersion
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber


logger = logging.getLogger('partcatalog')

def add_triac(part: Part, manufacturer):
    return Triac.objects.update_or_create(
        MPN=part.part_number,
        manufacturer=manufacturer
    )


part_type_map = {
    'Triac': add_triac
}

def import_part(part: Part):
    manufacturer = get_or_create_manufacturer_by_name(part.manufacturer)
    # Add part
    db_part, created = part_type_map[part.part_type](part, manufacturer)
    # Add part order numbers
    create_or_update_manufacturer_order_numbers(part, db_part)
    create_or_update_files(part, db_part)


def create_or_update_manufacturer_order_numbers(part: Part, db_part: Part_db):
    for name, order_number in part.order_numbers.values():
        try:
            logger.debug(f'Updating MON: {order_number.order_number} for part {db_part.MPN}')
            defaults = {
                "packaging": order_number.packaging,
                "part": db_part,
                "EAN13": order_number.EAN13,
                "SKU": order_number.SKU
            }
            if order_number.production_status:
                defaults["production_status"] = order_number.production_status

            ManufacturerOrderNumber.objects.update_or_create(
                MON=order_number.order_number,
                manufacturer=db_part.manufacturer,
                defaults=defaults
            )
        except Exception as e:
            logger.error(f"Exception {e}")


def create_or_update_files(part: Part, db_part: Part_db):
    output_dir = Path(settings.MEDIA_ROOT).joinpath('part_catalog', 'docs')

    for key, attachment_file in part.files.items():
        defaults = {
          #  "url": attachment_file.url,
            "description": attachment_file.description,
            "file_type": attachment_file.type
        }
        file_obj, created = File.objects.update_or_create(
            name=attachment_file.filename,
            manufacturer = db_part.manufacturer,
            defaults=defaults
        )
        db_part.files.add(file_obj)

        for version_key, version in attachment_file.versions.items():
            file_extension = Path(version.filepath).suffix[1:]
            FileVersion.objects.update_or_create(
                file_container=file_obj,
                version=version.revision,
                defaults={
                    "publication_date": version,
                    "url": version,
                    "md5sum": version.md5sum,
                    "file": output_dir.joinpath(version.filename(db_part.manufacturer, db_part.MPN, file_extension))
                }
            )
    db_part.save()
