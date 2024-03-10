from django.contrib import admin
from .models import Distributor, DistributorOrderNumber, DistributorManufacturer

admin.site.register(Distributor)
admin.site.register(DistributorManufacturer)


@admin.register(DistributorOrderNumber)
class DistributorOrderNumberAdmin(admin.ModelAdmin):
    fields = ('distributor', 'don', 'mon', 'manufacturer_name', 'service')
    search_fields = ['distributor__name', 'don', 'service__name']
