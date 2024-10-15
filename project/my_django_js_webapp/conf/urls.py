# conf/urls.py
from django.contrib import admin
from django.urls import path, include
from rawsound import urls as rawsound
from common.views import index
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
    path('board/', include('boards.urls')),
    path('kisti/', include('sound.urls')),
    path('board/list/  #화면 샘플', include('boards.urls')),
    path('preprocessing/', include('preprocessing.urls')),
    path('evaluation_set/', include('evaluation_set.urls')),
    path('rawsound/', include((rawsound, 'rawsound'), namespace='rawsound')),
]

urlpatterns += static('/excel/', document_root='media/upload/excel/')