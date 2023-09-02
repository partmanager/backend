from django.urls import path

from . import views
from . import views_api as api

app_name = 'partcatalog'
urlpatterns = [
    path('api/get_part_menu', api.get_part_menu, name='api-get-part-menu'),
    path('api/get_part_list', views.api_get_part_list, name='api-get-part-list'),

    path('api/part/import', api.start_import, name='api-get-part-import')
]
