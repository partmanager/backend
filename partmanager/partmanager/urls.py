"""partmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from rest_framework.routers import DefaultRouter

from .views import export, ImportView, UpdateGitView, GenerateSymbolsView

from distributors.views import DistributorViewSet, DistributorOrderNumberViewSet, DistributorManufacturerViewSet, api_stock_and_price
from inventory.views import InventoryPositionViewSet, StrageLocationFolderViewSet
from inventory.api import StorageLocationWithItemsViewSet
from invoices.views import InvoiceViewSet, InvoiceImportView
from invoices.views import InvoiceItemViewSet, InvoiceItemWithStorageViewSet
from manufacturers.views_api import ManufacturerViewSet
from inventory.api import CategoryViewSet, StorageLocationViewSet, InventoryReservationViewSet
from projects.views_api import AssemblyViewSet, AssemblyJobViewSet, BOMViewSet, BOMItemViewSet, ProjectViewSet, ProjectVersionViewSet, BOMImportView, GenerateAssemblyViewSet, AssemblyItemViewSet
from partcatalog.views import ManufacturerOrderNumberViewSet, PartPolimorphicViewSet


router = DefaultRouter()
router.register(r'api/distributor', DistributorViewSet, basename='Distributor')
router.register(r'api/distributor-order-number', DistributorOrderNumberViewSet, basename='DistributorOrderNumberViewSet')
router.register(r'api/distributor-manufacturer', DistributorManufacturerViewSet, basename='DistributorManufacturer')
router.register(r'api/inventory', InventoryPositionViewSet, basename='InventoryPositionViewSet')
router.register(r'api/inventory-category', CategoryViewSet, basename='CategoryViewSet')
router.register(r'api/inventory-reservation', InventoryReservationViewSet, basename='InventoryReservationViewSet')
router.register(r'api/invoice', InvoiceViewSet, basename='Invoice')
router.register(r'api/invoiceItem', InvoiceItemViewSet, basename='InvoiceItem')
router.register(r'api/invoiceItemWithStorage', InvoiceItemWithStorageViewSet, basename='InvoiceItemStorage')
router.register(r'api/manufacturer', ManufacturerViewSet, basename='ManufacturerViewSet')
router.register(r'api/storage_location', StorageLocationViewSet, basename='StorageLocationViewSet')
router.register(r'api/storage_location_items', StorageLocationWithItemsViewSet, basename='StorageLocationWithItemsViewSet')
router.register(r'api/storage_location_folder', StrageLocationFolderViewSet, basename='StorageLocationFolderViewSet')
router.register(r'api/project', ProjectViewSet, basename='ProjectViewSet')
router.register(r'api/project-version', ProjectVersionViewSet, basename='ProjectVersionViewSet')
router.register(r'api/bom', BOMViewSet, basename='BOMViewSet')
router.register(r'api/bom-item', BOMItemViewSet, basename='BOMItemViewSet')
router.register(r'api/assembly-job', AssemblyJobViewSet, basename='AssemblyJobViewSet')
router.register(r'api/assembly', AssemblyViewSet, basename='AssemblyViewSet')
router.register(r'api/assembly-item', AssemblyItemViewSet, basename='AssemblyItemViewSet')




router.register(r'api/part/mon', ManufacturerOrderNumberViewSet, basename='ManufacturerOrderNumberViewSet')

router.register(r'api/part-poli', PartPolimorphicViewSet, basename='PartPolimorphicViewSet')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/bom-import/', BOMImportView.as_view(), name='bom-import'),
    path('api/distributor/stock_and_price/', api_stock_and_price, name='DistributorStockAndPrice'),
    path('manufacturers/', include('manufacturers.urls')),
    path('distributors/', include('distributors.urls')),
    path('inventory/', include('inventory.urls')),
    path('invoices/', include('invoices.urls')),
    path('api/invoiceImport', InvoiceImportView.as_view()),
    path('parts/', include('partcatalog.urls')),
    path('api/assembly-job-generate/<int:pk>/', GenerateAssemblyViewSet.as_view()),
    path('projects/', include('projects.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='inventory/', permanent=True)),
    path('import', ImportView.as_view(), name='import'),
    path('export', export),
    path('updategit', UpdateGitView.as_view(), name='updategit'),
    path('symbolsgen', GenerateSymbolsView.as_view(), name='symbolsgen'),
    url(r'^', include(router.urls)),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


