# conf/urls.py
from django.urls import path
from .views import evaluation_set_list, new_data_set_upload, select_existing_source_data, existing_source_data_selection_excel_download

urlpatterns = [
    path('list/', evaluation_set_list, name='evaluation_set_list'),
    path('new_data_set_upload/', new_data_set_upload, name='new_data_set_upload'),
    path('select_existing_source_data/', select_existing_source_data, name='select_existing_source_data'),
    path('existing_source_data_selection_excel_download/', existing_source_data_selection_excel_download, name='existing_source_data_selection_excel_download'),
]