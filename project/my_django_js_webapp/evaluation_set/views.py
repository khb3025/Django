from django.shortcuts import render
from sound.models import Metadata, Detail, Noise
from django.http import Http404, HttpResponse, JsonResponse
from common.views import file_upload, excel_download

# Create your views here.

def evaluation_set_list(request):
    
    if request.method == 'POST':
        data_list = list(
            Metadata.objects.filter(
                data_set_idx=2
            ).prefetch_related(
                'noise', 
                'detail'
            ).values(
                'noise__ni_info',
                'cre_dt'
            )
        )
        
        return JsonResponse({'data': data_list})
    return render(request, 'evaluation_set_list.html')


def select_existing_source_data(request):

    if request.method == 'POST':
        data_list = list(
            Metadata.objects.filter(
                data_set_idx=2
            ).prefetch_related(
                'noise', 
                'detail'
            ).values(
                'noise__ni_info',
                'cre_dt'
            )
        )
        
        return JsonResponse({'data': data_list})

    return render(request, 'evaluation_set_list.html')


def existing_source_data_selection_excel_download(request):
    
    data_list = list(Metadata.objects.all().values('cre_dt', 'data_set_idx', 'version'))

    excel_header_list = [
        '일자',
        'idx',
        'version'
    ]

    sheet_name = 'sample_list'

    save_path, save_name = excel_download(data_list=data_list, excel_header_list=excel_header_list, sheet_name=sheet_name)

    return JsonResponse({'success': True, 'save_path': save_path, 'file_name': save_name})


def new_data_set_upload(request):
    
    file = request.FILES.get('files')

    file_upload_success_flag = file_upload(None, file, None, None, None, None, None)

    msg = 'file upload 실패' if not file_upload_success_flag else 'file upload 성공'

    return JsonResponse({'success': file_upload_success_flag, 'msg': msg})