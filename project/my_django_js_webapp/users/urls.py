# users/urls.py

from django.urls import path
from .views import register_user, user_login, user_logout, get_csrf, get_user_info, login_view

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('csrf/', get_csrf, name='api-csrf'),
    path('user_info/', get_user_info, name='api-user_info'),
    path('login_view/', login_view, name='login_view'),
]
