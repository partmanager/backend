from django.contrib import admin

# Register your models here.
from .models import Project, ProjectVersion, BOM, BOMItem, Assembly, AssemblyItem

admin.site.register(Project)
admin.site.register(ProjectVersion)
admin.site.register(BOM)
admin.site.register(BOMItem)
admin.site.register(Assembly)
admin.site.register(AssemblyItem)
