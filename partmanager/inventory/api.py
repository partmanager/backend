from .models import InventoryPosition, Category, StorageLocation, StorageLocationFolder, InventoryReservation
from django.db.models import Sum
from django.http import JsonResponse
from invoices.models import InvoiceItem
from invoices.serializers import InvoiceItemDetailSerializer
from manufacturers.serializers import ManufacturerSerializer
from manufacturers.models import Manufacturer
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber
from partcatalog.utils import get_part
from .barcode_decoder.barcode_decoder import decode_barcode
import json
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, StorageLocationSerializer, StorageLocationDetailSerializer, \
    InventoryReservationSerializer, StorageLocationWithItemsSerializer


def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data:
            inventory_position = InventoryPosition.objects.get(pk=data['id'])
            if inventory_position.stock == data['initial_quantity']:
                inventory_position.stock = data['quantity']
                inventory_position.save_with_history(comment=data['comment'] if 'comment' in data else None,
                                                     user_id=request.user.id)
                print(request.user.id)
                return JsonResponse({'status': 'OK',
                                     'quantity': inventory_position.stock,
                                     'unit': 'pcs'})
        else:
            print('invalid data')
            return JsonResponse({'status': 'Error', 'message': "Error"})


def flat_category_list(request):
    def process_children(childrens, path):
        categorys = []
        for children in childrens:
            new_path = path + ' \u27A4 ' + children.name
            categorys.append({'id': children.pk,
                              # 'label': children.name,
                              'name': new_path})
            categorys.extend(process_children(children.category_set.all(), new_path))
        return categorys

    category_root = Category.get_root()

    category = [{'id': category_root.pk,
                 'name': "Root"}]
    category.extend(process_children(category_root.category_set.all(), "Root"))
    return JsonResponse({'categories': category})


# def storage_location_folders_list(request):
#     locations = StorageLocationFolder.objects.all()
#     rows = []
#     for location in locations:
#         rows.append({'name': location.name, 'id': location.pk})
#     return JsonResponse({'rows': rows})


def storage_location_flat_list(request):
    objects_list = StorageLocation.objects.all()
    locations = []
    for location in objects_list:
        locations.append(location.to_dict())
    return JsonResponse({'storage_locations': locations})


def storage_location_list(request):
    empty_only = request.GET.get('empty_only', None)
    print(empty_only)

    if empty_only == 'true':
        storage_locations = StorageLocation.objects.annotate(
            quantity=Sum('inventoryposition__stock')
        ).filter(quantity=0, folder__isnull=True)
    else:
        storage_locations = StorageLocation.objects.filter(folder__isnull=True)

    locations_without_folder = []
    for location in storage_locations:
        locations_without_folder.append(location.to_dict())

    locations = StorageLocationFolder.to_dict()
    locations.append({'name': 'Unassigned',
                      'id': 10001,
                      'selectable': False,
                      'children': locations_without_folder})
    return JsonResponse({'name': 'root',
                         'id': 10000,
                         'selectable': False,
                         'children': locations})


def storage_location_detail(request, pk):
    storage_location = StorageLocation.objects.get(pk=pk)

    rows = []
    for part in storage_location.inventoryposition_set.all():
        rows.extend(part.to_view_ajax_response())
    response = {'id': storage_location.pk,
                'name': storage_location.location,
                "rows": rows
                }
    return JsonResponse(response, safe=False)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer


class StorageLocationViewSet(ModelViewSet):
    queryset = StorageLocation.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update']:
            return StorageLocationDetailSerializer
        return StorageLocationSerializer


class StorageLocationWithItemsViewSet(ModelViewSet):
    queryset = StorageLocation.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StorageLocationWithItemsSerializer


class InventoryReservationViewSet(ModelViewSet):
    queryset = InventoryReservation.objects.all()
    serializer_class = InventoryReservationSerializer


def assign_missing_mon(request):
    inventory_items = InventoryPosition.objects.filter(part__isnull=True)
    found_count = 0
    for inventory in inventory_items:
        found = get_part(manufacturer=inventory.manufacturer,
                         manufacturer_part_number=None,
                         manufacturer_order_number=inventory.name)
        if found and found['mon'] is not None:
            found_count += 1
            inventory.part = found['mon']
            inventory.save()
    return JsonResponse({'missing_part': len(inventory_items), 'found': found_count})


def add_item_barcode_search(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if 'barcode' in data:
            data = data['barcode']
        if data:
            item = decode_barcode(data)
            print(item)
            assert len(item) <= 1
            item = item[0]

            new_item_candidate = {'stock': item['quantity'],
                                  'stock_unit': 1,
                                  'condition': 'n',
                                  'status': 'b',
                                  'name': item['manufacturer_order_number']}
            don = item['distributor_order_number']['don']
            if don:
                new_item_candidate['distributor_id'] = don.distributor.pk
                new_item_candidate['don'] = don.don
                if don.mon:
                    manufacturer = ManufacturerSerializer(don.mon, read_only=True)
                    new_item_candidate['manufacturer'] = manufacturer.data
                    manufacturer_order_number = don.mon
                    part_type = manufacturer_order_number.part.part_type
                    default_categories = Category.objects.filter(default_part_types__contains=[part_type])
                    if len(default_categories) > 0:
                        print(default_categories)
                        new_item_candidate['category_id'] = default_categories[0].pk

            if item['invoice']:
                invoice = InvoiceItemDetailSerializer(item['invoice'], read_only=True)
                new_item_candidate['invoice'] = invoice.data

            return JsonResponse(new_item_candidate)


def flag_unflag_components(request, pk):
    flag = request.GET.get('flag', None)
    if flag is not None:
        inventory_position = InventoryPosition.objects.get(pk=pk)
        if flag == 'true':
            inventory_position.flagged = True
            inventory_position.save()
        elif flag == 'false':
            inventory_position.flagged = False
            inventory_position.save()
        return JsonResponse({'status': "OK", 'message': 'Flag changed'})


def flag_all_components(request):
    InventoryPosition.objects.update(flagged=True)
    return JsonResponse({'status': "OK", 'message': 'All items flagged'})


def archive_or_unarchive_component(request, pk):
    flag = request.GET.get('archive', None)
    if flag is not None:
        inventory_position = InventoryPosition.objects.get(pk=pk)
        if flag == 'true':
            inventory_position.archived = True
        else:
            inventory_position.archived = False
        inventory_position.save()
        return JsonResponse({'status': "OK", 'message': 'Archive flag changed'})
