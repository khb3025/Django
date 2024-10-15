# conf/urls.py
from django.urls import path
from .views import evaluation_set_list

urlpatterns = [
    path('list/', evaluation_set_list, name='evaluation_set_list'),
]