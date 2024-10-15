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
   

]