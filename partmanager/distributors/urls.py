from django.urls import path

from . import views

app_name = 'distributors'
urlpatterns = [
    path('api/update/', views.update, name='api-update')
]
