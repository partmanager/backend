from django.urls import path

from . import views_api as api

app_name = 'projects'
urlpatterns = [
    path('api/get_projects_menu', api.projects_menu, name='api-projects-menu')
]
