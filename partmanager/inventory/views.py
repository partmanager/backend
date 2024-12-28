from .models import InventoryPosition, InventoryPositionHistory, Category, StorageLocationFolder, InventoryReservation
from .forms import InventoryPositionStockQuantityCommentForm
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers_simple import StorageLocationFolderSerializer
from .tasks import update_inventory_mpn_assignments
from .serializers import InventoryPositionSerializer, InventoryPositionHistorySerializer, InventoryPositionCreateSerializer, InventoryPositionMinimalSerializer, InventoryReservationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class InventoryPositionViewSet(ModelViewSet):
    queryset = InventoryPosition.objects.all()
    serializer_class = InventoryPositionSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'part__manufacturer_order_number', 'storage_location__location']
    filterset_fields = {'category': ['in'], 'archived': ['exact'], 'flagged': ['exact']}

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InventoryPositionCreateSerializer
        return InventoryPositionSerializer


class PartLocationsViewSet(ModelViewSet):
    queryset = InventoryPosition.objects.all()
    serializer_class = InventoryPositionMinimalSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'part__manufacturer_order_number', 'storage_location__location']
    filterset_fields = {'mon__part': ['exact'], 'mon': ['exact'], 'archived': ['exact'], 'flagged': ['exact']}


class StrageLocationFolderViewSet(ModelViewSet):
    queryset = StorageLocationFolder.objects.all()
    serializer_class = StorageLocationFolderSerializer



class CategoryFilterSet(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        result = {}
        for category in queryset:
            result[category.pk] = category.get_id_set()
        return Response(result, status=200)


def api_category_list(request):
    def process_children(childrens, path):
        childrens_processed = []
        for children in childrens:
            new_path = path + ' ' + children.name
            childrens_processed.append({'id': children.pk,
                                        'label': children.name,
                                        'path': new_path,
                                        'children': process_children(children.category_set.all(), new_path)})
        return childrens_processed
    category_root = Category.get_root()

    category = {'id': category_root.pk,
                'label': category_root.name,
                'path': "Root",
                'children': process_children(category_root.category_set.all(), "Root")}
    return JsonResponse(category, safe=False)


def inventory_stock_update(request, pk):
    if request.method == 'POST':
        form = InventoryPositionStockQuantityCommentForm(request.POST)
        if form.is_valid():
            inventory_position = InventoryPosition.objects.get(pk=pk)
            inventory_position.stock = form.cleaned_data['stock']
            inventory_position.save_with_history(comment=form.cleaned_data['comment'], user_id=request.user.id)
            print(request.user.id)
            return JsonResponse({'status': 'OK',
                                 'quantity': inventory_position.stock,
                                 'unit': 'pcs'})
        else:
            print('invalid form', form)
            return JsonResponse({'status': 'Error', 'message': "Error"})


def inventory_position_history_list_view(request, pk):
    history_list = InventoryPositionHistory.objects.filter(inventory_position__pk=pk).order_by('-version')
    serializer = InventoryPositionHistorySerializer(history_list, many=True)
    return JsonResponse({"rows": serializer.data})


def update(request):
    update_inventory_mpn_assignments.delay()
    return JsonResponse({"status": "OK"})
