from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models.common import Package
from .serializers import PackagePolymorphicSerializer


class PackagePolimorphicViewSet(ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackagePolymorphicSerializer
    pagination_class = PageNumberPagination
    search_fields = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'name': ["in", "exact"],
        'type': ["exact"]
    }