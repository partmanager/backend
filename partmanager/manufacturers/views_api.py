from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Manufacturer
from rest_framework.viewsets import ModelViewSet
from .serializers import ManufacturerSerializer, ManufacturerDetailSerializer


class ManufacturerViewSet(ModelViewSet):
    serializer_class = ManufacturerSerializer
    search_fields = ['number', 'distributor__name']
    queryset = Manufacturer.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update']:
            return ManufacturerDetailSerializer
        return ManufacturerSerializer


def detail(request, pk):
    # if request.is_ajax():
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    return JsonResponse({'id': manufacturer.pk,
                         'name': manufacturer.name, 'full_name': manufacturer.full_name,
                         'address': manufacturer.address, 'website': manufacturer.website,
                         'email': manufacturer.email,
                         'phone': manufacturer.phone, 'comment': manufacturer.comment,
                         'partCount': manufacturer.part_count(),
                         'orderNumberCount': manufacturer.order_number_count(),
                         'seriesData': manufacturer.series()})

