from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from common.views import file_upload
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import datetime
import traceback
import json
import logging
import uuid
import os
log = logging.getLogger(__name__)

# Create your views here.
def multipart_upload_page(request):
    context = {}
    return render(request,'file_upload_examples/multipart_upload_page.html',context)

def multipart_upload(request):
    context = {}
    try:
        multi_files = request.FILES.getlist('multi_upload')
        save_path = settings.UPLOAD_URL
        # file_upload()
        ###### upload 방법 1. ######
        # 파일 처리 (Basic한 처리)
        # for file in multi_files:
        #     # 파일을 저장하는 코드 예시
        #     with open(f'{save_path}/{file.name}', 'wb+') as destination:
        #         for chunk in file.chunks():
        #             destination.write(chunk)
        # context["status"] = True
        
        ###### upload 방법 2. #####
        # uuid, 확장자 등 처리
        upload_complete= files_upload(files=multi_files)
        if upload_complete:
            context["success"] = True
        return JsonResponse(context)
    
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = trace_back
        return JsonResponse(context,status=500)

                  
def files_upload(files: list,
                 file_reg_gb: str = None, 
                 file_real_name: str = None, 
                 file_ext: str = None, 
                 file_size: str = None, 
                 target_pk: str = None,
                 reg_user_no: str = None):
    
    '''파일 객체를 받아 서버에 저장한다.

    Args:
        file_reg_gb (str): 파일을 저장시키는 테이블 구분
        file (list): File 객체의 리스트
        file_real_name (str): file 업로드시, 이름
        file_ext (str): file 확장자
        file_size (str): file 크기
        target_pk (str): 파일을 저장시킬때의 테이블 번호
        reg_user_no (str): 등록 회원 번호

    Returns:
        True or False: 업로드 성공시, True 실패시, False를 반환
    '''
    try:
        save_path = settings.UPLOAD_URL

        for file in files :
            file_name = str(uuid.uuid4()).replace('-', '')
            fs = FileSystemStorage(
                location=save_path
            )
            file_origin_name = os.path.splitext(file.name)[0]
            file_extension = os.path.splitext(file.name)[1]
            fs.save(file_name + file_extension, file)

        return True
    
    except Exception as e:
        log.info( traceback.format_exc() )
        log.info('save_path :::::::::: %s', save_path)
        return False