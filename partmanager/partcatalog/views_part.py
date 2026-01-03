from rest_framework.viewsets import ModelViewSet
from .models.resistor import Resistor
from .part_serializers import ResistorSerializer, ResistorCreateSerializer
from common.pagination import StandardResultsSetPagination


class ResistorViewSet(ModelViewSet):
    queryset = Resistor.objects.all()
    serializer_class = ResistorCreateSerializer
    pagination_class = StandardResultsSetPagination