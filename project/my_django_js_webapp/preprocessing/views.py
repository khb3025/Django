from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from sound.models import Metadata, Noise, Detail
from django.forms.models import model_to_dict
from django.db import transaction, connection
from django.db.models import Q, F, CharField, Func, Value
from django.db.models.functions import Cast, Coalesce

from .model_form import MetadataForm, NoiseForm, DetailForm
from django.contrib import messages
import datetime
import traceback
import json
        
def preprocessing_list_page(request):
    context = {}
    return render(request,'preprocessing/preprocessing_list.html', context)
# 전처리 목록 가져오기
def get_preprocessing_list(request):
    context = {}
    try:
        orm_list_obj = Metadata.objects.all().annotate(
            snd_set_idx = F('detail__snd_set_idx'),
            snd_cate = F('detail__snd_cate'),
            snd_sub_cate = F('detail__snd_sub_cate'),
            snd_ni_db = F('detail__snd_ni_db'),
            snd_cmnt = F('detail__snd_cmnt')
        ).values(
            'snd_set_idx',
            'media_url',
            'reg_dt',
            'snd_cate',
            'snd_sub_cate',
            'version', # 이상치 값 대용 (임시)
            'lp_data_len', # 파일 길이 값 대용
            'snd_ni_db', # dB 값 대용
            'snd_cmnt' # 상태 값 대용
        )
        result_list = list(orm_list_obj)
        
        # for item in result_list:
        #     for key, value in item.items():
        #         if isinstance(value,datetime.datetime) :
        #             print("reg_dt value type >>>",type(value))
        #             item[key] = value.strftime("%Y/%m/%d %H:%M")
        #         else:
        #             item[key] = value if value is not None else ""
        # print("result list >>>",result_list)
        
        context['data'] = result_list 
        return JsonResponse(context)
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = trace_back
        return JsonResponse(context)  
    

def preprocessing(request):
    context = {}
    try:
        id_list = json.loads(request.body)
        print("id_list >>>", id_list)
        with transaction.atomic():
            detail_objs = Detail.objects.filter(snd_set_idx__in=id_list)
            for obj in detail_objs:
                obj.snd_cmnt = "완료"   
            Detail.objects.bulk_update(detail_objs, ['snd_cmnt'])
        
        context["success"] = True
        context["msg"] = "전처리 완료"
        return JsonResponse(context)
    
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "전처리 에러"
        return JsonResponse(context,status=500)  


def preprocessing_delete(request):
    context = {}
    try:
        id_list = json.loads(request.body)
        print("id_list >>>", id_list)
        with transaction.atomic():
            detail_objs = Detail.objects.filter(snd_set_idx__in=id_list)
            for obj in detail_objs:
                obj.snd_cmnt = "삭제"   
            Detail.objects.bulk_update(detail_objs, ['snd_cmnt'])
        
        context["success"] = True
        context["msg"] = "삭제 완료"
        return JsonResponse(context)
    
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "삭제 에러"
        return JsonResponse(context,status=500)  

# Test Code
def meta_intro(request):
    context = {}
    return render(request,'sample/meta_data/meta_intro.html', context)

def meta_list(request):
    context = {}
    meta_result = Metadata.objects.all().values(
        'data_set_idx'
        ,'data_set'
        ,'version'
        ,'media_url'
        ,'cre_dt'
        ,'ado_result'
        ,'bit_dep'
        ,'sam_rte'
        ,'rec_strime'
        ,'tdms_flag'
        ,'file_path'
        ,'daq_sam_rte'
        ,'x_pixel'
        ,'y_pixel'
        ,'ip_cam_x_slop'
        ,'ip_cam_y_slop'
        ,'beam_wid'
        ,'beam_hei'
        ,'lp_data'
        ,'lp_data_idx'
        ,'lp_data_len'
        ,'lp_data_file_path'
        ,'img_data'
        ,'img_idx'
        ,'img_file_path'
        ,'beam_pwr'
        ,'beam_pwr_idx'
        ,'beam_pwr_path'
        ,'img_video_path'
        ,'beam_video_path'
        ,'video_path'
        ,'reg_user'
        ,'reg_dt'
    )
    context['meta_list'] = list(meta_result)
    return render(request,'sample/meta_data/meta_list.html', context)
    
def meta_detail(request, data_set_idx):
    context = {}
    meta_data = Metadata.objects.filter(data_set_idx=data_set_idx).values()
    if meta_data.exists():
        meta_data = meta_data[0]
    print("meta detail >>>", meta_data)
    context['meta_data'] = dict(meta_data)
    return render(request,'sample/meta_data/meta_detail.html', context)

def meta_update_page(request, data_set_idx):
    context = {}
    meta_data = Metadata.objects.filter(data_set_idx=data_set_idx).values()
    if meta_data.exists():
        meta_data = meta_data[0]
    print("meta detail >>>", meta_data)
    context['meta_data'] = dict(meta_data)
    return render(request,'sample/meta_data/meta_update_page.html', context)

def meta_insert_page(request):
    context = {}
    return render(request, 'sample/meta_data/meta_insert_page.html', context)

def meta_insert(request):
    context = {}
    try:
        data_dict = {
            'data_set': request.POST.get('data_set'),
            'media_url': request.POST.get('media_url'),
            'cre_dt' : datetime.datetime.now(),
            'version': request.POST.get('version'),
            'ado_result': request.POST.get('ado_result'),
            'bit_dep': request.POST.get('bit_dep'),
            'sam_rte': request.POST.get('sam_rte'),
            'rec_strime': request.POST.get('rec_strime'),
            'tdms_flag': request.POST.get('tdms_flag'),
            'file_path': request.POST.get('file_path'),
            'daq_sam_rte': request.POST.get('daq_sam_rte'),
            'x_pixel': request.POST.get('x_pixel'),
            'y_pixel': request.POST.get('y_pixel'),
            'ip_cam_x_slop': request.POST.get('ip_cam_x_slop'),
            'ip_cam_y_slop': request.POST.get('ip_cam_y_slop'),
            'beam_wid': request.POST.get('beam_wid'),
            'beam_hei': request.POST.get('beam_hei'),
            'lp_data': request.POST.get('lp_data'),
            'lp_data_idx': request.POST.get('lp_data_idx'),
            'lp_data_len': request.POST.get('lp_data_len'),
            'lp_data_file_path': request.POST.get('lp_data_file_path'),
            'img_data': request.POST.get('img_data'),
            'img_idx': request.POST.get('img_idx'),
            'img_file_path': request.POST.get('img_file_path'),
            'beam_pwr': request.POST.get('beam_pwr'),
            'beam_pwr_idx': request.POST.get('beam_pwr_idx'),
            'beam_pwr_path': request.POST.get('beam_pwr_path'),
            'img_video_path': request.POST.get('img_video_path'),
            'beam_video_path': request.POST.get('beam_video_path'),
            'video_path': request.POST.get('video_path'),
            'reg_user': request.POST.get('reg_user'),
        }
        
        meta_form = MetadataForm(data_dict)
        if meta_form.is_valid():
            meta_save_obj = meta_form.save()
            return redirect(reverse('meta_detail',args=[meta_save_obj.data_set_idx]))
        else :
            print("error param >>>", meta_form.errors)
            # 각 필드의 오류를 확인하고 메시지를 추가
            error_messages = []
            for field, errors in meta_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\\n".join(error_messages)
            raise CustomMessageException(f"Metadata 입력값 에러 : \\n{alert_message}")
        
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print("meta_insert trace_back >>>", trace_back)
        print("meta_insert message >>>", e.message)
        messages.error(request, e.message)
        return redirect(reverse('meta_insert_page'))
    
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("def meta_insert 에러")
        messages.error(request, "def meta_insert 에러")
        return redirect(reverse('meta_insert_page'))

def meta_update(request, data_set_idx):
    context = {}
    try :
    
        data_dict = {
            'data_set_idx' : data_set_idx,
            
            'data_set': request.POST.get('data_set'),
            'version' : request.POST.get('version'),
            'media_url': request.POST.get('media_url'),
            'ado_result': request.POST.get('ado_result'),
            'bit_dep': request.POST.get('bit_dep'),
            'sam_rte': request.POST.get('sam_rte'),
            
            'rec_strime': request.POST.get('rec_strime'),
            'tdms_flag': request.POST.get('tdms_flag'),
            'file_path': request.POST.get('file_path'),
            'daq_sam_rte': request.POST.get('daq_sam_rte'),
            'x_pixel': request.POST.get('x_pixel'),
            
            'y_pixel': request.POST.get('y_pixel'),
            'ip_cam_x_slop': request.POST.get('ip_cam_x_slop'),
            'ip_cam_y_slop': request.POST.get('ip_cam_y_slop'),
            'beam_wid': request.POST.get('beam_wid'),
            'beam_hei': request.POST.get('beam_hei'),
            
            'lp_data': request.POST.get('lp_data'),
            'lp_data_idx': request.POST.get('lp_data_idx'),
            'lp_data_len': request.POST.get('lp_data_len'),
            'lp_data_file_path': request.POST.get('lp_data_file_path'),
            'img_data': request.POST.get('img_data'),
            
            'img_idx': request.POST.get('img_idx'),
            'img_file_path': request.POST.get('img_file_path'),
            'beam_pwr': request.POST.get('beam_pwr'),
            'beam_pwr_idx': request.POST.get('beam_pwr_idx'),
            'beam_pwr_path': request.POST.get('beam_pwr_path'),
            
            'img_video_path': request.POST.get('img_video_path'),
            'beam_video_path': request.POST.get('beam_video_path'),
            'video_path': request.POST.get('video_path'),
            'reg_user' : request.POST.get('reg_user'),
        }
        
        meta_instance = get_object_or_404(Metadata, data_set_idx=data_set_idx)
        meta_form = MetadataForm(data_dict, instance=meta_instance)
        
        if meta_form.is_valid():
            meta_data = Metadata.objects.filter(data_set_idx=data_set_idx)
            if meta_data.exists():
                meta_form.save()
            else:
                raise CustomMessageException("존재하지 않는 Metadata 정보")
        else :
            print("error param >>>", meta_form.errors)
            # 각 필드의 오류를 확인하고 메시지를 추가
            error_messages = []
            for field, errors in meta_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\\n".join(error_messages)
            raise CustomMessageException(f"Metadata 입력값 에러 : \\n{alert_message}")
        
        return redirect(reverse('meta_detail',args=[data_set_idx]))
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print("meta_update trace_back >>>", trace_back)
        print("meta_update message >>>", e.message)
        messages.error(request, e.message)
        return redirect(reverse('meta_update_page',args=[data_set_idx]))
    
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("def meta_update 에러")
        messages.error(request, "def meta_update 에러")
        return redirect(reverse('meta_update_page',args=[data_set_idx]))
    
def meta_delete(request, data_set_idx):
    context = {}
    meta_data = Metadata.objects.filter(data_set_idx=data_set_idx)
    if meta_data.exists():
        meta_data = meta_data[0]
    meta_data.delete()
    return redirect(reverse('meta_list'))


#####################################
def noise_list(request, meta_data_idx):
    context = {}
    noise_list = Noise.objects.filter(data_set_idx=meta_data_idx).values()
    context['noise_list'] = list(noise_list)
    context['meta_data_idx'] = meta_data_idx
    print("noise_list >>>", list(noise_list))
    return render(request, 'sample/noise/noise_list.html', context)


def noise_insert_page(request, meta_data_idx) :
    context = {}
    context["meta_data_idx"] = meta_data_idx
    return render(request, 'sample/noise/noise_insert_page.html', context)

def noise_insert(request):
    context = {}
    try :
        # ni_info = request.POST.get("ni_info")
        # ni_bg_cate = request.POST.get("ni_bg_cate")
        # ni_bg_sub_cate = request.POST.get("ni_bg_sub_cate")
        # ni_place = request.POST.get("ni_place")
        # ni_bg_sdb = request.POST.get("ni_bg_sdb")
        # ni_bg_luf = request.POST.get("ni_bg_luf")
        # ni_device = request.POST.get("ni_device")
        # ni_len = request.POST.get("ni_len")
        # meta_data_idx = int(request.POST.get("meta_data_idx"))
        
        r_param = json.loads(request.body)
        print("noise_insert r_param >>>", r_param)
        # noise_form = NoiseForm(r_param)
        noise_form = NoiseForm(r_param)
        if noise_form.is_valid():
            fk_meta_obj = Metadata.objects.filter(data_set_idx = r_param['data_set_idx'])
            if fk_meta_obj.exists():
                new_noise = noise_form.save()
                # new_noise = Noise.objects.create(
                #     ni_info = ni_info,
                #     data_set_idx = fk_meta_obj,
                #     ni_bg_cate = ni_bg_cate,
                #     ni_bg_sub_cate = ni_bg_sub_cate,
                #     ni_place = ni_place,
                #     ni_bg_sdb = ni_bg_sdb,
                #     ni_bg_luf = ni_bg_luf,
                #     ni_device = ni_device,
                #     ni_len = ni_len
                # )
                result_dict = model_to_dict(new_noise)
                print("Noise result_dict >>>", result_dict)
                context["msg"] = "success"
                context["data"] = result_dict
            else :
                CustomMessageException("부모 객체(meta_data)가 존재하지 않습니다.")
        else: 
            error_messages = []
            for field, errors in noise_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\n".join(error_messages)
            raise CustomMessageException(f"Noise 입력값 에러 : \n{alert_message}")
        
        return JsonResponse(context)
    
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context['msg'] = e.message
        return JsonResponse(context,status=500)
    
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "Noise Insert Error"
        return JsonResponse(context,status=500)
    
def noise_detail(request):
    context ={}
    try:
        ni_set_idx=request.GET.get("ni_set_idx")
        print("noise_detail ni_set_idx >>>", ni_set_idx)
        noise = Noise.objects.get(ni_set_idx=ni_set_idx)
        context["noise_obj"] = noise
        return render(request, 'sample/noise/noise_detail.html', context)
    except Exception as e :
        meta_data_idx = request.GET.get("data_set_idx")
        trace_back = traceback.format_exc()
        print("noise_detail trace_back >>>", trace_back)
        return redirect(reverse('meta_detail', args=[meta_data_idx]))
    
def noise_update_page(request, ni_set_idx):
    context ={}
    try:
        print("noise_update_page ni_set_idx >>>", ni_set_idx)
        noise = Noise.objects.get(ni_set_idx=ni_set_idx)
        context["noise_obj"] = noise
        return render(request, 'sample/noise/noise_update_page.html', context)
    except Exception as e :
        meta_data_idx = request.GET.get("data_set_idx")
        trace_back = traceback.format_exc()
        print("noise_detail trace_back >>>", trace_back)
        return redirect(reverse('meta_detail', args=[meta_data_idx]))        

def noise_update(request):
    context={}
    try:
        r_param = json.loads(request.body)
        noise = Noise.objects.get(ni_set_idx=r_param['ni_set_idx'])
        noise_form = NoiseForm(r_param, instance=noise)
        if noise_form.is_valid():
            parent_obj= Metadata.objects.filter(data_set_idx=r_param['data_set_idx'])
            if parent_obj.exists():
                update_noise_obj = noise_form.save()
                noise_dict = model_to_dict(update_noise_obj)
                context["data"] = noise_dict
            else :
                raise CustomMessageException("부모 객체(Meta)가 존재하지 않습니다.")
        else :
            error_messages = []
            for field, errors in noise_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\n".join(error_messages)
            raise CustomMessageException(f"Noise 입력값 에러 : \n{alert_message}")
        
        context["msg"] = "success"
        return JsonResponse(context)
    
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context['msg'] = e.message
        return JsonResponse(context,status=500)
    
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "Noise Update Error"
        return JsonResponse(context,status=500)


def noise_delete(request, ni_set_idx):
    try:
        noise_obj = Noise.objects.get(ni_set_idx=int(ni_set_idx))
        noise_obj.delete()
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
    finally :
        meta_data_idx = request.GET.get('data_set_idx')
        return redirect(reverse('noise_list',args=[meta_data_idx]))
    
    
    # ni_set_idx
    
    # ni_info
    # ni_bg_cate
    # ni_bg_sub_cate
    # ni_place
    # ni_bg_sdb
    # ni_bg_luf
    # ni_device
    # ni_len
    # data_set_idx_id
    
    
#################################################
def sound_detail_list(request, meta_data_idx):
    context = {}
    detail_list = Detail.objects.filter(data_set_idx=meta_data_idx)
    context['s_detail_list'] = detail_list
    context['meta_data_idx'] = meta_data_idx
    return render(request, 'sample/sound_detail/sound_detail_list.html', context)

def sound_detail_insert_page(request, meta_data_idx):
    context = {}
    context['meta_data_idx'] = meta_data_idx
    return render(request, 'sample/sound_detail/sound_detail_insert_page.html', context)

def sound_detail_insert(request):
    context = {}
    try :
        request_p = None
        detail_form = DetailForm(json.loads(request.body))
        if detail_form.is_valid():
            request_p = json.loads(request.body)
            with transaction.atomic():
                is_exist_meta = Metadata.objects.filter(data_set_idx = request_p['data_set_idx'])
                if is_exist_meta.exists():
                    insert_S_D_obj= detail_form.save()
                    context['sound_detail_obj'] = model_to_dict(insert_S_D_obj)
                    return JsonResponse(context)
                else :
                    raise CustomMessageException("부모 객체(meta_data)가 존재하지 않습니다.")
        else :
            error_messages = []
            for field, errors in detail_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\n".join(error_messages)
            raise CustomMessageException(f"sound_detail 입력값 에러 : \n{alert_message}")
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = e.message
        return JsonResponse(context,status=500)
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "def sound_detail_insert Error"
        return JsonResponse(context,status=500)

def sound_detail(request, meta_data_idx):
    context = {}
    try:
        snd_set_idx = request.GET.get("snd_set_idx")
        s_d_obj = Detail.objects.filter(snd_set_idx=snd_set_idx)
        if s_d_obj.exists():
            context['s_d_obj'] = model_to_dict(s_d_obj[0])
        else:
            raise CustomMessageException("소리 상세 정보가 없습니다.")
        
        print("context >>>", context)
        return render(request, 'sample/sound_detail/sound_detail.html' ,context)
    
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("sound_detail Server Error")
        return redirect(reverse('sound_detail_list',args=[meta_data_idx]))
    
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("sound_detail Error Msg >>>", e.message)
        return redirect(reverse('sound_detail_list',args=[meta_data_idx]))

def sound_detail_update_page(request, meta_data_idx):
    context = {}
    try:
        snd_set_idx = request.GET.get("snd_set_idx")
        s_d_obj = Detail.objects.filter(snd_set_idx=snd_set_idx)
        if s_d_obj.exists():
            context['s_d_obj'] = model_to_dict(s_d_obj[0])
        else:
            raise CustomMessageException("소리 상세 정보가 없습니다.")
        
        print("context >>>", context)
        return render(request, 'sample/sound_detail/sound_detail_update_page.html' ,context)

    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("sound_detail Error Msg >>>", e.message)
        return redirect(reverse('sound_detail_list',args=[meta_data_idx]))
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        print("sound_detail Server Error")
        return redirect(reverse('sound_detail_list',args=[meta_data_idx]))


def sound_detail_update(request):
    context = {}
    try:
        request_p = json.loads(request.body)
        detail_instance = get_object_or_404(Detail, snd_set_idx=request_p['snd_set_idx'])
        detail_form = DetailForm(request_p, instance=detail_instance)
        if detail_form.is_valid():
            with transaction.atomic():
                is_exist_meta = Metadata.objects.filter(data_set_idx = request_p['data_set_idx'])
                if is_exist_meta.exists():
                    update_S_D_obj= detail_form.save()
                    context['data'] = model_to_dict(update_S_D_obj)
                    return JsonResponse(context)
                else :
                    raise CustomMessageException("부모 객체(meta_data)가 존재하지 않습니다.")  
        else :
            error_messages = []
            for field, errors in detail_form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            alert_message = "\n".join(error_messages)
            raise CustomMessageException(f"sound_detail 입력값 에러 : \n{alert_message}")
        
    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = e.message
        return JsonResponse(context,status=500)
    except Exception as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "def sound_detail_insert Error"
        return JsonResponse(context,status=500)
    

def sound_detail_delete(request):
    context = {}
    try :
        request_p = json.loads(request.body)
        print("sound_detail delete >>>", request_p)
        del_detail_obj = Detail.objects.filter(snd_set_idx=request_p['snd_set_idx'])
        if del_detail_obj.exists():
            del_detail_obj = del_detail_obj[0]
            del_detail_obj.delete()
            context["msg"] = "성공적으로 삭제되었습니다."
            return JsonResponse(context)
        else :
            raise CustomMessageException("삭제하려는 소리상세 정보가 존재하지 않습니다.")

    except CustomMessageException as e:
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = e.message
        return JsonResponse(context,status=500)
    
    except Exception as e :
        trace_back = traceback.format_exc()
        print(trace_back)
        context["msg"] = "def sound_detail_delete Error"
        return JsonResponse(context,status=500) 
    
class CustomMessageException(Exception):
    def __init__(self, message):
        self.message = message