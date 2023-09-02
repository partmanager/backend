from django.contrib import admin

# Register your models here.
from .models import InventoryPosition, StorageLocation, Category

admin.site.register(InventoryPosition)
admin.site.register(StorageLocation)
admin.site.register(Category)
