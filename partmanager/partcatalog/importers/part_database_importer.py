from .json_importer import json_importer
import logging

logger = logging.getLogger('partcatalog')


def import_form_file(file, dry=True):
    try:
        logger.info(f"Loading {file}")
        json_importer.parts_import(file)
        json_importer.run(dry=dry)
    except KeyError as e:
        logger.error(f"Invalid file (KeyError) {file} {e}")
