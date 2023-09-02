from .models.part import Part


from .models.manufacturer_order_number import ManufacturerOrderNumber
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ManufacturerOrderNumberSerializer
from .part_serializers import PartPolymorphicSerializer

menu = {"Passives": {"Balun": "/parts/balun", "Resistors": "/parts/0", "Capacitors": "/parts/1", "Inductors": "/parts/2", "Ferrite Bead": "/parts/8"},
        "Diodes": {"Small signal": "/parts/3", "LED": "/parts/4", "Bridge Rectifiers": "/parts/17"},
        "TVS": "/parts/5",
        "Cristal": "/parts/9",
        "Transistor Bipolar": "/parts/6",
        "Integrated Circuits": "/parts/7",
        "Connectors": {"Connector": "/parts/10"},
        "Modules": "/parts/11",
        "Enclosures": "/parts/12",
        "Battery": "/parts/16",
        "Battery Holders": "/parts/13",
        "Switch": '/parts/14'
        }


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class ManufacturerOrderNumberViewSet(ModelViewSet):
    queryset = ManufacturerOrderNumber.objects.all()
    pagination_class = StandardResultsSetPagination
    search_fields = ['manufacturer_order_number', 'part__manufacturer_part_number']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['manufacturer']


    def get_serializer_class(self):
        return ManufacturerOrderNumberSerializer


def fields_to_columns(fields):
    columns = []
    for field in fields:
        if field == 'MPN':
            columns.append({
                "field": fields[field],
                "title": field,
                "formatter": 'mpnFormatter'
            })
        else:
            columns.append({
                "field": fields[field],
                "title": field
            })
    return columns


def django_choices_to_dict(choices):
    entry = choices
    #for entry in choices:
    print(entry)
    entry_dict = dict(entry)
    result_dict = {}
    for entry in entry_dict:
        value = entry_dict[entry]
        if isinstance(value, tuple):
            result_dict[entry] = django_choices_to_dict(value)
        else:
            result_dict[value] = entry
    print("----------->", result_dict)
    return result_dict


class PartPolimorphicViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartPolymorphicSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['manufacturer_part_number', 'manufacturer_order_number_set__manufacturer_order_number']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'part_type': ["in", "exact"],
        'manufacturer': ["exact"]
    }


def api_get_part_list(request):
    object_list = ManufacturerOrderNumber.objects.all()
    search = request.GET.get('searchText', None)
    manufacturer = request.GET.get('manufacturer', None)
    if manufacturer:
        object_list = object_list.filter(manufacturer__pk=int(manufacturer))
    if search:
        object_list = object_list.filter(manufacturer_order_number__icontains=search)

    page_number = request.GET.get('pageNumber', None)
    page_size = request.GET.get('pageSize', None)
    paginator = Paginator(object_list, page_size)
    page = paginator.page(page_number)
    rows = []
    for part in page.object_list:
        rows.extend(part.to_ajax_response())
    response = {"total": paginator.count,
                "rows": rows}
    return JsonResponse(response, safe=False)

