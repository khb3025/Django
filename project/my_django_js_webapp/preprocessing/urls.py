from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sound.api import MetadataViewSet, DetaildataViewSet
from .views import *
# from .views import post_list, post_detail
router = DefaultRouter()
router.register(r'meta', MetadataViewSet)
#router.register(r'detail', DetaildataViewSet)
#router.register(r'noise', NoisedataViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    path('preprocessing_list_page/', preprocessing_list_page, name='preprocessing_list_page'),
    path('get_preprocessing_list/', get_preprocessing_list, name='get_preprocessing_list'),
    path('preprocessing/', preprocessing, name='preprocessing'),
    path('preprocessing_delete/', preprocessing_delete, name='preprocessing_delete'),
    path('get_origin_source_list/', get_origin_source_list, name='get_origin_source_list'),
    path('confirm_library_active/', confirm_library_active, name='confirm_library_active'),
    
    #waveSurfer Audio
    path('show_audio_wave/', show_audio_wave, name='show_audio_wave'),
    
    # TEST
    path('meta_intro/', meta_intro, name='meta_intro'),
    path('meta_list/', meta_list, name='meta_list'),
    path('meta_list/<int:data_set_idx>/', meta_detail, name='meta_detail'),
    path('meta_list/meta_insert_page/', meta_insert_page, name='meta_insert_page'),
    path('meta_list/meta_insert/', meta_insert, name='meta_insert'),
    path('meta_list/<int:data_set_idx>/update_page/', meta_update_page, name='meta_update_page'),
    path('meta_list/<int:data_set_idx>/update/', meta_update, name='meta_update'),
    path('meta_list/<int:data_set_idx>/delete/', meta_delete, name='meta_delete'),
    
    path('noise/<int:meta_data_idx>/noise_list/', noise_list , name='noise_list'),
    path('noise/<int:meta_data_idx>/noise_insert_page/', noise_insert_page , name='noise_insert_page'),
    path('noise/noise_insert/', noise_insert , name='noise_insert'),
    path('noise/noise_detail/', noise_detail , name='noise_detail'),
    path('noise/<int:ni_set_idx>/noise_update_page/', noise_update_page , name='noise_update_page'),
    path('noise/noise_update/', noise_update , name='noise_update'),
    path('noise/<int:ni_set_idx>/noise_delete/', noise_delete , name='noise_delete'),
    
    path('sound_detail/<int:meta_data_idx>/sound_detail_list/', sound_detail_list , name='sound_detail_list'),
    path('sound_detail/<int:meta_data_idx>/sound_detail_insert_page/', sound_detail_insert_page , name='sound_detail_insert_page'),
    path('sound_detail_insert/', sound_detail_insert, name='sound_detail_insert'),
    path('sound_detail/<int:meta_data_idx>/sound_detail' , sound_detail, name='sound_detail'),
    path('sound_detail/<int:meta_data_idx>/sound_detail_update_page' , sound_detail_update_page, name='sound_detail_update_page'),
    path('sound_detail/sound_detail_update' , sound_detail_update, name='sound_detail_update'),
    path('sound_detail/sound_detail_delete' , sound_detail_delete, name='sound_detail_delete'),

]