from .models import InventoryPosition, InventoryPositionHistory, Category
from .forms import InventoryPositionStockQuantityCommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .tasks import update_inventory_mpn_assignments

from .serializers import InventoryPositionSerializer, InventoryPositionDetailSerializer, InventoryPositionHistorySerializer


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
    search_fields = ['distributor_number', 'inventoryposition__part__manufacturer_order_number']
    filterset_fields = ['category', 'archived', 'flagged']

def api_inventory_list(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    search = request.GET.get('searchText', None)
    if search:
        object_list = InventoryPosition.objects.filter(Q(category__in=category.get_id_set()) &
                                                       (Q(name__icontains=search) |
                                                        Q(part__manufacturer_order_number__icontains=search) |
                                                        Q(description__icontains=search) |
                                                        Q(storage_location__location__icontains=search)))
    else:
        object_list = InventoryPosition.objects.filter(category__in=category.get_id_set())

    flagged = request.GET.get('flagged', None)
    if flagged is not None:
        flagged = True if flagged == 'true' else False
        object_list = object_list.filter(flagged=flagged)

    archived = request.GET.get('archived', None)
    if archived is not None:
        archived = True if archived == 'true' else False
        object_list = object_list.filter(archived=archived)

    page_number = request.GET.get('pageNumber', None)
    page_size = request.GET.get('pageSize', None)

    if page_number and page_size:
        if int(page_number) * int(page_size) > len(object_list):
            page_number = 1

    paginator = Paginator(object_list, page_size or 50)
    page = paginator.page(page_number or 1)
    rows = []    
    serializer = InventoryPositionDetailSerializer(page.object_list, many=True)
    rows = serializer.data    
    response = {"total": paginator.count,
                "rows": rows
                }
    return JsonResponse(response, safe=False)


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
