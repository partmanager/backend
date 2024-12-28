import logging
from django.conf import settings
import json

from distributors_api.mouser import Mouser
from distributors_api.tme import TME


logger = logging.getLogger('distributors')
__distributor_connectors = {}


def get_distributor_api_connector(distributor_name: str):
    logger.info(f"Accessing distributor connector: {distributor_name}")
    if distributor_name in __distributor_connectors:
        return __distributor_connectors[distributor_name]


def load_settings():
    try:
        logger.info("Loading distributor connector credintials")
        with open(file=settings.DISTRIBUTORS_CREDENTIALS_FILE) as f:
            distributors_api_config = json.load(f)
            if 'Mouser' in distributors_api_config:
                __distributor_connectors['Mouser'] = Mouser(distributors_api_config['Mouser'])
            elif 'TME' in distributors_api_config:
                __distributor_connectors['TME'] = TME(distributors_api_config['TME'])
    except FileNotFoundError as e:
        logger.warning(f"Unable to open distributors credential file: {e}")
