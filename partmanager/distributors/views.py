from django.http import JsonResponse
from .models import Distributor, DistributorOrderNumber, DistributorManufacturer
from .filters import DistributorOrderNumberFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import DistributorSerializer, DistributorDetailSerializer, DistributorOrderNumberSerializer,\
    DistributorOrderNumberDetailSerializer, DistributorManufacturerSerializer, DistributorManufacturerDetailSerializer, \
    DistributorManufacturerCreateSerializer
from .tasks import update_manufacturer_order_number


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class DistributorViewSet(ModelViewSet):
    serializer_class = DistributorSerializer
    queryset = Distributor.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistributorDetailSerializer
        return DistributorSerializer


class DistributorOrderNumberViewSet(ModelViewSet):
    queryset = DistributorOrderNumber.objects.all()
    serializer_class = DistributorOrderNumberSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['don', 'mon']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DistributorOrderNumberFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistributorOrderNumberDetailSerializer
        elif self.action == 'create':
            return DistributorOrderNumberDetailSerializer
        return DistributorOrderNumberSerializer


class DistributorManufacturerViewSet(ModelViewSet):
    serializer_class = DistributorManufacturerSerializer
    queryset = DistributorManufacturer.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['manufacturer__name']
    filterset_fields = ['distributor']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update']:
            return DistributorManufacturerDetailSerializer
        elif self.action == 'create':
            return DistributorManufacturerCreateSerializer
        return DistributorManufacturerSerializer


def api_stock_and_price(request):
        pk = request.GET.getlist('pk', None)
        refresh = request.GET.get('refresh', None)
        if refresh:
            refresh = bool(refresh)
        else:
            refresh = False
        print("Distributors", request, pk, refresh)
        if pk:
            objects = DistributorOrderNumber.objects.filter(pk__in=pk)
            if objects:
                distributor_pk_set = objects.values_list('distributor', flat=True)
                response = []
                for pk in distributor_pk_set:
                    distributor_objects = objects.filter(distributor__pk=pk)
                    distributor = distributor_objects[0].distributor
                    if refresh:
                        stock_and_price = distributor.request_stock_and_price(distributor_objects)
                    else:
                        stock_and_price = distributor.get_stock_and_price(distributor_objects)
                    response = stock_and_price
                return JsonResponse({"rows": response})


def update(request):
    update_manufacturer_order_number.delay()
    return JsonResponse({"status": "OK"})
