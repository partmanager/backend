from .models import Manufacturer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ManufacturerSerializer, ManufacturerDetailSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['name', 'full_name', 'comment', 'address']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ['in', 'exact'],
        'full_name': ['in', 'exact']
    }

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update']:
            return ManufacturerDetailSerializer
        return ManufacturerSerializer
