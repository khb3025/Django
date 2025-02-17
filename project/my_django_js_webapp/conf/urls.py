# conf/urls.py
from django.contrib import admin
from django.urls import path, include
from rawsound import urls as rawsound
from preprocessing import urls as preprocessing
from file_upload_examples import urls as file_upload_examples
from common.views import index
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
    path('kisti/', include('sound.urls')),
    path('preprocessing/', include((preprocessing, 'preprocessing'), namespace='preprocessing')),
    path('evaluation_set/', include('evaluation_set.urls')),
    path('rawsound/', include((rawsound, 'rawsound'), namespace='rawsound')),
    path('file_upload_examples/',include((file_upload_examples, 'file_upload_examples'), namespace='file_upload_examples')),
    path('api/', include('users.urls')),  #유저 부분 추가
]

urlpatterns += static('/excel/', document_root='media/upload/excel/')


