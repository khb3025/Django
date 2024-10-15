from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sound.api import MetadataViewSet, DetaildataViewSet
from .views import *
# from .views import post_list, post_detail
router = DefaultRouter()
router.register(r'meta', MetadataViewSet)
# router.register(r'detail', DetaildataViewSet)
# router.register(r'noise', NoisedataViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    path('multipart_upload_page', multipart_upload_page, name='multipart_upload_page'),
    path('multipart_upload', multipart_upload, name='multipart_upload'),

]