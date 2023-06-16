from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.list , name='list'),
    path('create/', views.create , name='restaurants-create'),
    path('update/', views.update , name='restaurants-update'),
    path('detail/', views.detail , name='restaurants-detail'),
    path('delete/',views.delete , name='restaurants-delete' )
]
