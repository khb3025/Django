# boards/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import sample_excel_download

urlpatterns = [
    path('sample/excel_download/', sample_excel_download, name='sample_excel_download'),
]
