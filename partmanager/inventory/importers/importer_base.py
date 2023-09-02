from inventory.models import InventoryPosition, StorageLocation, StorageLocationFolder, Category
from invoices.models import Invoice
import logging

logger = logging.getLogger('inventory')


class InventoryImporterBase:
    def find_invoice_item(self, invoice_data, manufacturer_order_number):
        if invoice_data:
            invoice = Invoice.get_by_invoice_number(invoice_data["Invoice Number"])
            if invoice:
                if len(invoice) == 1:
                    return invoice[0].get_item(manufacturer_order_number=manufacturer_order_number,
                                               distributor_order_number_text=invoice_data["Symbol"],
                                               position=invoice_data["Position"])

    def create_or_update_inventory_position(self, position_dict):
        position = InventoryPosition.from_dict(position_dict)
        position.save_with_history(comment=None, user_id=None)
        return position

    def create_or_update_storage_location(self, location_dict):
        location = StorageLocation.get_by_name(location_dict['name'])
        if location is None:
            return self.create_storage_location(location_dict)

    def create_storage_location(self, location_dict):
        logger.info(f"Crating location: {location_dict}")
        storage_location = StorageLocation()
        storage_location.location = location_dict['name']
        storage_location.description = location_dict['description']
        if 'folder_name' in location_dict and location_dict['folder_name'] is not None:
            folder = StorageLocationFolder.objects.filter(name=location_dict['folder_name'])
            if folder:
                storage_location.folder = folder[0]
            else:
                storage_location.folder = self.create_storage_location_folder(location_dict['folder_name'])
        storage_location.save()
        return storage_location

    def create_storage_location_folder(self, name):
        folder = StorageLocationFolder()
        folder.name = name
        folder.save()
        return folder

    def add_or_update_category(self, category_dict):
        logger.info(f"Add or update category, name: {category_dict['name']} path: {category_dict['path']}")
        category = self.get_category(category_dict)
        if category is None:
            logger.info("\tUnable to find category, creating...")
            category = self.create_category_recursive(category_dict)
            return category

    def get_category(self, category_dict):
        if category_dict['name'] == 'Root':
            return Category.get_root()
        else:
            category_list = Category.objects.filter(name=category_dict['name'], parent__name=category_dict['parent'])
            if len(category_list) == 1:
                category = category_list[0]
                if category.get_path() == category_dict['path']:
                    return category
            elif len(category_list) > 1:
                for category in category_list:
                    if category.get_path() == category_dict['path']:
                        return category

    def create_category_recursive(self, category_dict):
        assert category_dict['path'][0] == 'Root'

        category_parent = Category.get_root()
        for path in category_dict['path'][1:-1]:
            try:
                category_parent = category_parent.category_set.get(name=path)
            except Category.DoesNotExist:
                logger.info(f"\t\tUnable to find parent: {path} creating...")
                category_parent = Category(name=path, parent=category_parent)
                category_parent.save()

        category = Category(name=category_dict['name'])
        category.description = category_dict['description']
        category.default_part_types = category_dict['default_part_types'] if 'default_part_types' in category_dict else None
        print("Parent", category_parent)
        category.parent = category_parent
        category.save()
        return category
