import json
from .importer_base import InventoryImporterBase


class DirectoryImporter(InventoryImporterBase):
    def import_inventory(self, workdir):
        self.__process_storage_location_file(workdir + '/storage_locations.json')
        self.__process_categories_file(workdir + '/categories.json')
        self.__process_inventory_positions_file(workdir + '/inventory_positions.json')

    def __process_storage_location_file(self, storage_locations_filename):
        print("Importing storage locations", storage_locations_filename)
        with open(storage_locations_filename, 'r') as manufacturers_file:
            locations = json.load(manufacturers_file)
            for location in locations:
                self.create_or_update_storage_location(location)

    def __process_categories_file(self, categories_filename):
        print("Importing inventory categories", categories_filename)
        with open(categories_filename, 'r') as categories_file:
            categories = json.load(categories_file)
            for category in categories:
                self.add_or_update_category(category)

    def __process_inventory_positions_file(self, inventory_positions_filename):
        print("Importing inventory", inventory_positions_filename)
        with open(inventory_positions_filename, 'r') as inventory_positions_file:
            positions = json.load(inventory_positions_file)
            for position in positions:
                self.create_or_update_inventory_position(position)
