from django.contrib import admin
from .models import Distributor, DistributorOrderNumber, DistributorManufacturer

admin.site.register(Distributor)
admin.site.register(DistributorManufacturer)


@admin.register(DistributorOrderNumber)
class DistributorOrderNumberAdmin(admin.ModelAdmin):
    fields = ('distributor', 'distributor_order_number_text', 'manufacturer_order_number_text', 'manufacturer_name_text', 'service')
    search_fields = ['distributor__name', 'distributor_order_number_text', 'service__name']
