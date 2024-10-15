from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from . import views as test
from .api import MetadataViewSet

router = DefaultRouter()
router.register(r'metadata', MetadataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Metadata
    path('metadata_list/', test.metadata_list, name='metadata_list'),
    path('metadata_info/', test.metadata_info, name='metadata_form'),
    path('metadata_info/<int:data_set_idx>/', test.metadata_info, name='metadata_info'),
    path('create_metadata/', test.create_metadata, name='create_metadata'),
    path('update_metadata/<int:data_set_idx>/', test.update_metadata, name='update_metadata'),
    path('delete_metadata/<int:data_set_idx>/', test.delete_metadata, name='delete_metadata'),
    
    # Noise
    path('noise_info/<int:data_set_idx>/', test.noise_info, name='noise_info'),
    path('create_noise/<int:data_set_idx>/', test.create_noise, name='create_noise'),
    path('update_noise/<int:ni_set_idx>/', test.update_noise, name='update_noise'),
    path('delete_noise/<int:ni_set_idx>/', test.delete_noise, name='delete_noise'),
    
    
    # Detail
    path('detail_info/<int:data_set_idx>/', test.detail_info, name='detail_info'),
    path('create_detail/<int:data_set_idx>/', test.create_detail, name='create_detail'),
    path('update_detail/<int:snd_set_idx>/', test.update_detail, name='update_detail'),
    path('delete_detail/<int:snd_set_idx>/', test.delete_detail, name='delete_detail'),
]