from django.urls import path

from . import views_api as api

app_name = 'manufacturers'
urlpatterns = [
    path('detail/<int:pk>', api.detail, name='manufacturer-detail'),
]
