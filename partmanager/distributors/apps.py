from django.apps import AppConfig


class DistributorsConfig(AppConfig):
    name = 'distributors'

    def ready(self):
        from .connector.distributorApiConnector import load_settings
        load_settings()
