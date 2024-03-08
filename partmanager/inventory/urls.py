from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import api

app_name = 'inventory'
urlpatterns = [
    path('', RedirectView.as_view(url='parts/1', permanent=True), name='index'),
    path('history/<int:pk>', views.inventory_position_history_list_view, name='parts-history'),

    # path('api/list/<int:category_pk>', views.api_inventory_list, name='api-inventory-list'),
    path('api/category_list', views.api_category_list, name='api-category-list'),
    path('api/category_flat_list', api.flat_category_list, name='api-category-flat-list'),
    path('api/storage_location_list', api.storage_location_list, name='api-storage-location-list'),
    path('api/storage_location_flat_list', api.storage_location_flat_list, name='api-storage-location-list'),
    # path('api/storage_location/folders_list', api.storage_location_folders_list, name='api-storage-location-folders-list'),
    path('api/storage_location_detail/<int:pk>', api.storage_location_detail, name='api-storage-location-detail'),
    path('api/add_item', api.add_item, name='api-add-item'),
    path('api/update_item', api.update_item, name='api-update-item'),
    path('api/assign_missing_mon', api.assign_missing_mon, name='assign_missing_mon'),
    path('api/add_item_barcode_search', api.add_item_barcode_search, name='api-add-item-barcode-search'),
    path('api/update_quantity', api.update_quantity, name='api-update-quantity'),
    path('api/flag/all', api.flag_all_components, name='api-flag-all-components'),
    path('api/flag/<int:pk>', api.flag_unflag_components, name='api-flag-component'),
    path('api/archive/<int:pk>', api.archive_or_unarchive_component, name='api-archive-component'),
    path('api/update', views.update, name='api-update'),
]


