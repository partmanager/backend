from django.db import models
from django.utils.timezone import now
from partcatalog.models.part import Part
from .fields import ChoiceArrayField
from manufacturers.models import get_manufacturer_by_name
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from invoices.models import get_invoice_item
from django.contrib.auth import get_user_model
from django.conf import settings
from partmanager.choices import QuantityUnit
import logging

logger = logging.getLogger('inventory')


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    default_part_types = ChoiceArrayField(models.CharField(max_length=3, choices=Part.PART_TYPE), null=True, blank=True)

    class Meta:
        unique_together = ["name", "parent"]

    def get_id_set(self):
        def make_id_set(category):
            id_set = [category.pk]
            for item in category.category_set.all():
                id_set = id_set + make_id_set(item)
            return id_set

        return make_id_set(self)

    def to_dict(self):
        return {'name': self.name,
                'description': self.description,
                'parent': self.parent.name if self.parent else None,
                'path': self.get_path(),
                'default_part_types': self.default_part_types}

    def get_path(self):
        logger.debug(f"Path for {self.name}")

        def get_parent_recursive(category, path):
            if category is None:
                print("Category is none, path", path)
            path.insert(0, category.name)
            if category == self.get_root():
                return path
            else:
                return get_parent_recursive(category.parent, path)

        return get_parent_recursive(self, [])

    @staticmethod
    def get_default_category_for_part(part):
        category = Category.objects.filter(default_part_types__contains=[part.part_type])
        if len(category) == 1:
            return category[0]
        elif len(category) > 1:
            print("Error")
        return Category.get_root()

    @staticmethod
    def get_root():
        root_category, created = Category.objects.get_or_create(name='Root',
                                                                parent=None)
        return root_category

    @staticmethod
    def get_as_dict():
        def process_children(parent):
            result = {}
            if parent.category_set.all():
                for children in parent.category_set.all():
                    if parent.name not in result:
                        result[parent.name] = {'id': parent.id, 'submenu': process_children(children)}
                    else:
                        result[parent.name]['submenu'].update(process_children(children))
            else:
                result[parent.name] = {'id': parent.id}
            return result

        return process_children(Category.get_root())

    def __str__(self):
        return self.name


class InventoryPosition(models.Model):
    CONDITION_STATUS = (
        ('n', 'New'),
        ('u', 'Used'),
        ('r', 'Refurbished'),
        ('b', 'Broken'),
        ('k', 'Unknown'),
    )
    INVENTORY_STATUS = (
        ('r', 'Awaiting order'),
        ('u', 'Ordered'),
        ('s', 'Shipped'),
        ('b', 'In stock')
    )

    name = models.CharField(max_length=200, null=True, blank=True)  # used when part is null
    description = models.CharField(max_length=1000, null=True, blank=True)  # used when part is null
    note = models.CharField(max_length=1000, null=True, blank=True)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.PROTECT, null=True,
                                     blank=True)  # used when part is null
    part = models.ForeignKey('partcatalog.ManufacturerOrderNumber', on_delete=models.PROTECT, null=True, blank=True)
    storage_location = models.ForeignKey('StorageLocation', on_delete=models.PROTECT)
    invoice = models.ForeignKey('invoices.InvoiceItem', on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField(help_text='Current stock')
    stock_unit = models.IntegerField(choices=QuantityUnit.choices, default=QuantityUnit.PCS)
    condition = models.CharField(max_length=1, choices=CONDITION_STATUS, default='n')
    status = models.CharField(max_length=1, choices=INVENTORY_STATUS, default='b')
    category = models.ForeignKey('inventory.Category', on_delete=models.PROTECT)
    LOT = models.CharField(max_length=20, null=True, blank=True, verbose_name="Lot number")
    ECCN = models.CharField(max_length=20, null=True, blank=True, verbose_name="Export Control Classification Number")
    COO = models.CharField(max_length=20, null=True, blank=True, verbose_name="Country of origin")
    TARIC = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name="Integrated Tariff of the European Community")
    archived = models.BooleanField(default=False)  # archived parts are excluded from query's and views by default
    flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', '-archived', 'part']

    def get_stock_value_display(self):
        stock_value = self.get_stock_value()
        if stock_value:
            return "{:.2f} {}".format(stock_value['net'], stock_value['currency_display'])
        return "Backend Error"


    def get_stock_value(self):
        try:
            return {'net': self.invoice.unit_price.net * self.stock,
                    'currency_display': self.invoice.get_unit_price_currency_display()}
        except TypeError as exception:
            return None

    def get_reserved_quantity(self):
        count = 0
        for reservation in self.inventoryreservation_set.all():
            count += reservation.quantity
        return count

    def inventory_position_history(self):
        return InventoryPositionHistory.objects.filter(inventory_position=self).order_by('-version')

    def save_with_history(self, comment, user_id):
        original = InventoryPosition.objects.get(pk=self.pk) if self.pk else None
        self.save()

        # save InventoryPosition history
        if original is None or original.stock != self.stock or original.storage_location != self.storage_location:
            user = get_user_model().objects.get(id=user_id) if user_id is not None else None
            inventory_position_history = self.inventory_position_history()
            if not inventory_position_history:
                new_history = InventoryPositionHistory(inventory_position=self,
                                                       stock=self.stock,
                                                       storage_location=self.storage_location,
                                                       user=user,
                                                       comment="Added inventory position.")
                new_history.save()
            elif inventory_position_history[0].stock != self.stock or inventory_position_history[
                0].storage_location != self.storage_location:
                new_history = InventoryPositionHistory(inventory_position=self,
                                                       stock=self.stock,
                                                       storage_location=self.storage_location,
                                                       user=user,
                                                       comment=comment
                                                       )
                new_history.save()

    def to_dict(self):
        result = {'name': self.name,
                  'description': self.description,
                  'note': self.note,
                  'manufacturer': self.manufacturer.name if self.manufacturer else None,
                  'part': None,
                  'storage_location': self.storage_location.location if self.storage_location else None,
                  'invoice': None,
                  'stock': self.stock,
                  'reserved_quantity': self.get_reserved_quantity(),
                  'condition': self.condition,
                  'status': self.status,
                  'category': {'name': self.category.name,
                               'path': self.category.get_path()},
                  'archived': self.archived,
                  'flagged': self.flagged}
        if self.part is not None:
            result['part'] = {'manufacturer': self.part.manufacturer.name,
                              'order_number': self.part.manufacturer_order_number,
                              'description': self.part.part.description}
        if self.invoice is not None:
            result['invoice'] = {'distributor': self.invoice.get_distributor_display(),
                                 'invoice_number': self.invoice.invoice.number,
                                 'invoice_position': self.invoice.position_in_invoice}
        return result

    @staticmethod
    def from_dict(dictionary):
        def get_description(mon):
            if mon is None and dictionary['description'] is None:
                if 'part' in dictionary and dictionary['part'] is not None:
                    return dictionary['part']['description']
                else:
                    return None
            else:
                return dictionary['description']

        def get_name(mon):
            if mon is None and dictionary['name'] is None:
                return dictionary['part']['order_number']
            else:
                return dictionary['name']

        part_manufacturer = None
        manufacturer = None
        mon = None
        if dictionary['part'] is not None:
            part_manufacturer = get_manufacturer_by_name(dictionary['part']['manufacturer'])
            try:
                mon = ManufacturerOrderNumber.objects.get(manufacturer=part_manufacturer,
                                                          manufacturer_order_number=dictionary['part']['order_number'])
            except ManufacturerOrderNumber.DoesNotExist:
                mon = None

        if dictionary['manufacturer'] is not None:
            manufacturer = get_manufacturer_by_name(dictionary['manufacturer'])
        if part_manufacturer is not None and manufacturer is not None:
            # assert part_manufacturer == manufacturer, f"{part_manufacturer} {manufacturer} {dictionary}"
            if part_manufacturer != manufacturer:
                logger.error(
                    f"Error, manufacturers name mismatch, Part reports: {part_manufacturer}, components expect: {manufacturer}, dict{dictionary}")
                mon = None

        inventory_position = InventoryPosition()
        inventory_position.name = get_name(mon)
        inventory_position.description = get_description(mon)
        inventory_position.note = dictionary['note'] if 'note' in dictionary else None
        inventory_position.manufacturer = manufacturer or part_manufacturer
        inventory_position.part = mon
        inventory_position.storage_location = StorageLocation.objects.get(location=dictionary['storage_location'])
        inventory_position.invoice = get_invoice_item(dictionary['invoice']['invoice_number'],
                                                      dictionary['invoice']['invoice_position']) if dictionary[
                                                                                                        'invoice'] is not None else None
        inventory_position.stock = dictionary['stock']
        inventory_position.condition = dictionary['condition']
        inventory_position.status = dictionary['status']
        if dictionary['category']['name'] == 'Root':
            inventory_position.category = Category.get_root()
        else:
            #            print(dictionary['category'])
            category = Category.get_root()
            for index, path_entry in enumerate(dictionary['category']['path'][1:]):
                #                print(path_entry, category.get_path(), category.category_set.all(), index)
                category = category.category_set.get(name=path_entry)
            inventory_position.category = category
        inventory_position.archived = dictionary['archived']
        inventory_position.flagged = dictionary['flagged'] if 'flagged' in dictionary else False
        return inventory_position

    def get_name_display(self):
        if self.part:
            return self.part.manufacturer_order_number
        else:
            return self.name

    def get_manufacturer_display(self):
        if self.part:
            return self.part.manufacturer.name
        elif self.manufacturer:
            return self.manufacturer.name
        else:
            return None

    def __str__(self):
        if self.invoice:
            return "{} {}, location: {}, invoice: {} -> {}".format(self.get_name_display(),
                                                                   self.get_manufacturer_display(),
                                                                   self.storage_location.location,
                                                                   self.invoice.invoice.distributor.name,
                                                                   self.invoice.invoice.number)
        else:
            return "{} {} {}".format(self.get_name_display(),
                                     self.get_manufacturer_display(),
                                     self.storage_location.location)


class InventoryPositionHistory(models.Model):
    version = models.IntegerField(editable=False)
    timestamp = models.DateTimeField(default=now, editable=False)
    inventory_position = models.ForeignKey('InventoryPosition', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    stock = models.IntegerField(help_text='Current stock', null=True, blank=True)
    storage_location = models.ForeignKey('StorageLocation', on_delete=models.PROTECT, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def to_dict(self):
        return {'version': self.version,
                'date': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'inventory_position_pk': self.inventory_position.pk,
                'stock': self.stock,
                'storage_location': self.storage_location.location,
                'user': str(self.user),
                'comment': self.comment}

    def save(self, *args, **kwargs):
        # start with version 1 and increment it for each book
        current_version = InventoryPositionHistory.objects.filter(inventory_position=self.inventory_position).order_by(
            '-version')[:1]
        self.version = current_version[0].version + 1 if current_version else 1
        super(InventoryPositionHistory, self).save(*args, **kwargs)


class StorageLocationFolder(models.Model):
    name = models.CharField(max_length=100, unique=True)

    @staticmethod
    def to_dict():
        locations = []
        for storage_location_folder in StorageLocationFolder.objects.all():
            childrens = []
            for children in storage_location_folder.storagelocation_set.all():
                childrens.append({'name': children.location, 'id': children.id})
            locations.append({'name': storage_location_folder.name,
                              'id': 100000 + storage_location_folder.id,
                              'selectable': False,
                              'children': childrens})
        return locations


class StorageLocation(models.Model):
    location = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True,
                                   help_text='Enter a brief description of storage location')
    folder = models.ForeignKey('inventory.StorageLocationFolder', on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def get_by_name(name):
        locations = StorageLocation.objects.filter(location=name)
        if len(locations) == 1:
            return locations[0]

    def to_dict(self):
        return {'id': self.pk,
                'name': self.location,
                'description': self.description,
                'folder_name': self.folder.name if self.folder else None}

    def __str__(self):
        return str(self.location)


class InventoryReservation(models.Model):
    quantity = models.FloatField()
    inventory = models.ForeignKey('inventory.InventoryPosition', on_delete=models.CASCADE)
    assembly = models.ForeignKey('projects.AssemblyItem', on_delete=models.CASCADE)

    class Meta:
        unique_together = ["inventory", "assembly"]
