import logging
from django.conf import settings
import json

from .mouser import Mouser
from .tme import TME


logger = logging.getLogger('distributors')
__distributor_connectors = {}


def get_distributor_api_connector(distributor_name: str):
    if distributor_name in __distributor_connectors:
        return __distributor_connectors[distributor_name]


def load_settings():
    pass
    try:
        with open(file=settings.DISTRIBUTORS_CREDENTIALS_FILE) as f:
            distributors_api_config = json.load(f)
            if 'Mouser' in distributors_api_config:
                __distributor_connectors['Mouser'] = Mouser(distributors_api_config['Mouser']["api_key"])
            elif 'TME' in distributors_api_config:
                __distributor_connectors['TME'] = TME(distributors_api_config['Mouser']['token'],
                                                      distributors_api_config['Mouser']['app_secret'])
    except FileNotFoundError as e:
        logger.warning(f"Unable to open distributors credential file: {e}")
