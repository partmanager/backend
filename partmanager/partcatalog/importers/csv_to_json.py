from .csv_to_json_base import CSVToJsonBase
from .json_importer import json_importer


class CSVToJson(CSVToJsonBase):
    def run(self, dry=False):
        json_importer.parts = self.get_parts_list()
        json_importer.run(dry)
