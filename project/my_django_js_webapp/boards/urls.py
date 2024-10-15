# boards/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import PostViewSet
from .views import post_list, post_detail

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
