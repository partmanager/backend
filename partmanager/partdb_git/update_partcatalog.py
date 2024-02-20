import logging
from distributors.importers.directory_importer import import_distributor
from manufacturers.importers.directory_importer import import_manufacturers
from partcatalog.tasks import import_components


# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('partdb_git')


def update_manufacturers(directory):
    logger.info(f"Updating manufacturers data")
    import_manufacturers(directory + "/manufacturers")


def update_distributors(directory):
    logger.info(f"Updating distributors data")
    import_distributor(directory + "/distributors")


def update_partcatalog(modified_files, progress_recorder):
    logger.info(f"Importing components")
    logger.debug(f"Modified files: {modified_files}")
    import_components(modified_files, progress_recorder)
