from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('select/', views.select ,name='select'),
    path('result/', views.result,name='result'),
    #path('select/<int:year>/' , views.select, name='select')
    #re_path(r'^select/(?P<year>[0-9]{4})/$',views.select , name='select')
]


