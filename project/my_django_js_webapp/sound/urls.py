from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import MetadataViewSet,DetaildataViewSet,NoisedataViewSet

router = DefaultRouter()
router.register(r'meta', MetadataViewSet)
router.register(r'detail', DetaildataViewSet)
router.register(r'noise', NoisedataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
