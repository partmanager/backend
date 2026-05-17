import logging
from django.conf import settings
from pathlib import Path

from partsdb_tools.components.Part import Part
from partsdb_tools.components.OrderNumber import ProductionStatus as PartsdbProductionStatus
from partsdb_tools.components.File import AttachmentType as PartsdbAttachmentType
from manufacturers.models import get_or_create_manufacturer_by_name
from partcatalog.models.integrated_circuit import IntegratedCircuit
from partcatalog.models.electronics_parts.triac import Triac
from partcatalog.models.part import Part as Part_db
from partcatalog.models.files import AttachmentType, File, FileVersion
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.models.choices import ProductionStatus


logger = logging.getLogger('partcatalog')

def add_triac(part: Part, manufacturer):
    try:
        part_obj = Triac.objects.get(
            MPN=part.part_number,
            manufacturer=manufacturer
        )
        return part_obj, None
    except Triac.DoesNotExist:
        part_obj = Triac(
            MPN=part.part_number,
            manufacturer=manufacturer
        )
        return part_obj, True
    finally:
        print('finally')


def add_vr(part: Part, manufacturer):
    try:
        part_obj = IntegratedCircuit.objects.get(
            MPN=part.part_number,
            manufacturer=manufacturer
        )
        return part_obj, None
    except IntegratedCircuit.DoesNotExist:
        part_obj = IntegratedCircuit(
            MPN=part.part_number,
            manufacturer=manufacturer
        )
        return part_obj, True
    finally:
        print('finally')
    

part_type_map = {
    'Triac': add_triac,
    'VoltageRegulator:Linear': add_vr
}

def import_part(part: Part):
    manufacturer = get_or_create_manufacturer_by_name(part.manufacturer)
    # Add part
    db_part, created = part_type_map[part.part_type](part, manufacturer)
    if created:
        db_part.save()
    # Add part order numbers
    create_or_update_manufacturer_order_numbers(part, db_part)
    create_or_update_files(part, db_part)
    create_or_update_pictures(part, db_part)


def convert_production_status(partsdb_production_status: PartsdbProductionStatus):
    convert = {
        PartsdbProductionStatus.UNKNOWN: ProductionStatus.UNKNOWN,
        PartsdbProductionStatus.PREVIEW: ProductionStatus.PREVIEW,
        PartsdbProductionStatus.IN_PRODUCTION: ProductionStatus.IN_PRODUCTION,
        PartsdbProductionStatus.NRD: ProductionStatus.NRD,
        PartsdbProductionStatus.LTB: ProductionStatus.LTB,
        PartsdbProductionStatus.OBSOLETE: ProductionStatus.OBSOLETE
    }
    return convert[partsdb_production_status]


def convert_attachment_type(partsdb_attachment_type: PartsdbAttachmentType):
    convert = {
        PartsdbAttachmentType.OTHER: AttachmentType.OTHER,
        PartsdbAttachmentType.APPLICATION_NOTE: AttachmentType.APPLICATION_NOTE,
        PartsdbAttachmentType.CALCULATION_TOOL: AttachmentType.CALCULATION_TOOL,
        PartsdbAttachmentType.DATASHEET: AttachmentType.DATASHEET,
        PartsdbAttachmentType.USER_MANUAL: AttachmentType.USER_MANUAL,
        PartsdbAttachmentType.REFERENCE_DESIGN: AttachmentType.REFERENCE_DESIGN,
        PartsdbAttachmentType.SERVICE_MANUAL: AttachmentType.SERVICE_MANUAL
    }
    return convert[partsdb_attachment_type]


def create_or_update_manufacturer_order_numbers(part: Part, db_part: Part_db):
    print("Creating MPNs", len(part.order_numbers))
    for name, order_number in part.order_numbers.values():
        try:
            print(name)
            print(order_number)
            print(f'Updating MON: {order_number.order_number} for part {db_part.MPN}')
            logger.debug(f'Updating MON: {order_number.order_number} for part {db_part.MPN}')
            defaults = {
                "packaging": order_number.packaging,
                "product": db_part,
                "EAN13": order_number.EAN13,
                "SKU": order_number.SKU
            }
            if order_number.production_status:
                defaults["production_status"] = convert_production_status(order_number.production_status)

            mon, created = ManufacturerOrderNumber.objects.update_or_create(
                MON=order_number.order_number,
                manufacturer=db_part.manufacturer,
                defaults=defaults
            )
            if created:
                print("Created MON")
                mon.save()
        except Exception as e:
            logger.error(f"Exception {e}")


def create_or_update_files(part: Part, db_part: Part_db):
    output_dir = Path().joinpath('part_catalog', 'docs')

    for attachment_file in part.files:
        defaults = {
          #  "url": attachment_file.url,
            "description": attachment_file.description,
            "file_type": convert_attachment_type(attachment_file.type)
        }
        file_obj, created = File.objects.update_or_create(
            name=attachment_file.filename,
            manufacturer = db_part.manufacturer,
            defaults=defaults
        )
        db_part.files.add(file_obj)

        for version_key, version in attachment_file.versions.items():
            file_extension = Path(version.filepath).suffix[1:]
            file_version, created = FileVersion.objects.update_or_create(
                file_container=file_obj,
                version=version.revision,
                defaults={
                    "publication_date": version,
                    "url": version,
                    "md5sum": version.md5sum
                },
                create_defaults={
                    "file__name": str(
                        output_dir.joinpath(version.filename(db_part.manufacturer.name, db_part.MPN, file_extension)))
                }
            )
    db_part.save()


def create_or_update_pictures(part: Part, db_part: Part_db):
    part.load_pictures()
    missing = []
    consumed = []
    need_save = False
    if db_part.images:
        for picture in part.pictures:
            found = False
            for db_picture in db_part.images:
                if picture.name == db_picture:
                    consumed.append(db_picture)
                    found = True
            if not found:
                missing.append(picture)
        # delete old/unused pictures
        for picture in db_part.images:
            if picture not in consumed:
                need_save = True
                pass # delete file from storage
        db_part.images = consumed

    # add missing pictures
    for picture in missing:
        need_save = True
        db_part.images.append(picture)
        # copy picture to storage

    if need_save:
        db_part.save()
