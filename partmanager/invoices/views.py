import os
import tempfile

from .models import Invoice, InvoiceItem
from rest_framework import status
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import InvoiceSerializer, InvoiceItemSerializer, InvoiceItemDetailSerializer, InvoiceItemCreateSerializer, InvoiceItemDetailWithStorageSerializer, InvoiceCreateSerializer
from .tasks import update_invoice_item_don_assignments, import_invoice_from_file
from .filters import InvoiceItemFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class InvoiceViewSet(ModelViewSet):
    """
    Used by frontend to display invoice list
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['number', 'distributor__name']
    filterset_fields = ['distributor', 'bookkeeping']
    queryset = Invoice.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return InvoiceCreateSerializer
        return InvoiceSerializer


class InvoiceItemViewSet(ModelViewSet):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['distributor_order_number__don', 'inventoryposition__part__manufacturer_order_number']
    filterset_fields = ['invoice__distributor', 'bookkeeping']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return InvoiceItemCreateSerializer
        return InvoiceItemDetailSerializer


class InvoiceItemWithStorageViewSet(ModelViewSet):
    """
    Used by frontend to display invoice items
    """
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['distributor_number', 'inventoryposition__part__manufacturer_order_number']
    filterset_class = InvoiceItemFilter

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update']:
            return InvoiceItemDetailWithStorageSerializer
        elif self.action == 'create':
            return InvoiceItemCreateSerializer
        return InvoiceItemDetailWithStorageSerializer


class InvoiceImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        importer = request.data['importer']
        invoice_import_file = request.FILES['file']
        distributor_name = request.data['distributor']
        invoice_date = request.data['invoice_date']

        if importer not in ['Archive importer', 'TME CSV file importer', 'Generic CSV file importer']:
            return Response({'error': 'Incorrect importer'}, status=status.HTTP_400_BAD_REQUEST)

        fd, tmp_invoice_import_file = tempfile.mkstemp()
        with open(tmp_invoice_import_file, 'wb') as f:
            content = invoice_import_file.read()
            f.write(content)
        os.close(fd)

        result = import_invoice_from_file.delay(importer, tmp_invoice_import_file, distributor_name, invoice_date)
        return Response({'task_id': result.task_id})


def update(request):
    result = update_invoice_item_don_assignments.delay()
    return Response({'task_id': result.task_id})
