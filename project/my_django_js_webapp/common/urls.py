# boards/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import sample_excel_download, sample_page, go_main

urlpatterns = [
    path('sample/excel_download/', sample_excel_download, name='sample_excel_download'),
    path('sample/', sample_page, name='sample_page'),
    path('main/', go_main, name='go_main'),
]
