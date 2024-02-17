from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api/invoice_items_options', api.invoice_items_options_list, name='api-invoice-items-options'),
    path('api/update', views.update, name='api-update'),
]
