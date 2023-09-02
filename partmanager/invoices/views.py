from django.http import JsonResponse
from .models import Invoice, InvoiceItem
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework import filters
from .importers.archive_importer import ArchiveInvoiceImporter
from .importers.tme_csv_importer import TMECSVImporter
from .importers.generic_csv_importer import GenericCSVImporter
from .serializers import InvoiceSerializer, InvoiceDetailSerializer, InvoiceItemSerializer, InvoiceItemDetailSerializer, InvoiceItemCreateSerializer, InvoiceWithItemsSerializer
from .tasks import update_invoice_item_don_assignments


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000


class InvoiceViewSet(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = InvoiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['number', 'distributor__name']
    queryset = Invoice.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update']:
            return InvoiceDetailSerializer
        return InvoiceSerializer


class InvoiceWithItemsViewSet(ModelViewSet):
    queryset = Invoice.objects.all()

    def get_serializer_class(self):
        return InvoiceWithItemsSerializer


class InvoiceItemViewSet(ModelViewSet):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['distributor_number', 'inventoryposition__part__manufacturer_order_number']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update']:
            return InvoiceItemDetailSerializer
        elif self.action == 'create':
            return InvoiceItemCreateSerializer
        return InvoiceItemDetailSerializer


def api_invoice_detail(request, pk):
    #if request.is_ajax():
        invoice = Invoice.objects.get(pk=pk)
        invoice_items = invoice.invoiceitem_set.all()
        items = []
        for invoice_item in invoice_items:
            items.extend(invoice_item.to_view_ajax_response())
        response = {"invoice": invoice.to_view_ajax_response(),
                    "items": items
                    }
        return JsonResponse(response, safe=False)


class InvoiceImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        importer = request.data['importer']
        invoice_import_file = request.FILES['file']
        print(importer)
        print(invoice_import_file)
        if importer == 'Archive importer':
            importer = ArchiveInvoiceImporter()
            result_invoice_model = importer.import_invoice(invoice_import_file)
        elif importer == 'TME CSV file importer':
            importer = TMECSVImporter()
            result_invoice_model = importer.import_invoice(invoice_import_file)
        elif importer == 'Generic CSV file importer':
            importer = GenericCSVImporter()
            distributor_name = request.cleaned_data['distributor']
            invoice_date = request.cleaned_data['invoice_date']
            result_invoice_model = importer.import_invoice(distributor_name, invoice_date, invoice_import_file)

        if result_invoice_model is not None:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'Error'})


def update(request):
    update_invoice_item_don_assignments.delay()
    return JsonResponse({"status": "OK"})
