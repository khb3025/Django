from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.crypto import get_random_string
from sound.models import Detail, Metadata, Noise


# START: Sound Metadata
def metadata_list(request):
    context = {}

    all_metadata = Metadata.objects.all()
    context['all_metadata'] = all_metadata
    
    return render(request, 'metadata/metadata_list.html', context)


def metadata_info(request, data_set_idx=None):
    context = {}
    
    if data_set_idx:
        context['metadata'] = get_object_or_404(Metadata, data_set_idx=data_set_idx)
        context['noise_list'] = Noise.objects.filter(data_set_idx=data_set_idx)
    
    return render(request, 'metadata/metadata_info.html', context)
    

def create_metadata(request):
    Metadata.objects.create(
        data_set = request.POST.get('data_set'),
        version = request.POST.get('version'),
        media_url = request.POST.get('media_url'),
        ado_result = request.POST.get('ado_result'),
        bit_dep = int(request.POST.get('bit_dep')),
        rec_strime = request.POST.get('rec_strime'),
        tdms_flag = request.POST.get('tdms_flag'),
        reg_user = request.POST.get('reg_user'),
    )
    
    return redirect('rawsound:metadata_list')


def update_metadata(request, data_set_idx):
    target_metadata = get_object_or_404(Metadata, data_set_idx=data_set_idx)
    target_metadata.data_set = request.POST.get('data_set')
    target_metadata.version = request.POST.get('version')
    target_metadata.media_url = request.POST.get('media_url')
    target_metadata.ado_result = request.POST.get('ado_result')
    target_metadata.bit_dep = int(request.POST.get('bit_dep'))
    target_metadata.rec_strime = request.POST.get('rec_strime')
    target_metadata.tdms_flag = request.POST.get('tdms_flag')
    target_metadata.reg_user = request.POST.get('reg_user')
    target_metadata.save()
    
    return redirect(reverse('rawsound:metadata_info', args=[data_set_idx]))


def delete_metadata(request, data_set_idx):
    target_metadata = get_object_or_404(Metadata, data_set_idx=data_set_idx)
    target_metadata.delete()
    
    return redirect('rawsound:metadata_list')
# END: Sound Metadata



# START: Sound Noise
def noise_info(request, data_set_idx):
    context = {}
    
    context['metadata'] = get_object_or_404(Metadata, data_set_idx=data_set_idx)
    
    noise_list = Noise.objects.filter(data_set_idx=data_set_idx)
    context['noise_list'] = noise_list
    
    return render(request, 'metadata/noise_info.html', context)


def create_noise(request, data_set_idx):
    Noise.objects.create(
        data_set_idx = get_object_or_404(Metadata, data_set_idx=data_set_idx),
        ni_info = request.POST.get('ni_info'),
        ni_bg_cate = request.POST.get('ni_bg_cate'),
        ni_bg_sub_cate = request.POST.get('ni_bg_sub_cate'),
        ni_place = request.POST.get('ni_place'),
        ni_bg_sdb = request.POST.get('ni_bg_sdb'),
        ni_bg_luf = request.POST.get('ni_bg_luf'),
        ni_device = request.POST.get('ni_device'),
        ni_len = int(request.POST.get('ni_len')),
    )
    
    return redirect(reverse('rawsound:noise_info', args=[data_set_idx]))


def update_noise(request, ni_set_idx):
    target_noise = get_object_or_404(Noise, ni_set_idx=ni_set_idx)
    target_noise.ni_info = request.POST.get('ni_info')
    target_noise.ni_bg_cate = request.POST.get('ni_bg_cate')
    target_noise.ni_bg_sub_cate = request.POST.get('ni_bg_sub_cate')
    target_noise.ni_place = request.POST.get('ni_place')
    target_noise.ni_bg_sdb = request.POST.get('ni_bg_sdb')
    target_noise.ni_bg_luf = request.POST.get('ni_bg_luf')
    target_noise.ni_device = request.POST.get('ni_device')
    target_noise.ni_len = int(request.POST.get('ni_len'))
    target_noise.save()
    
    data_set_idx = target_noise.data_set_idx.data_set_idx
    
    return redirect(reverse('rawsound:noise_info', args=[data_set_idx]))


def delete_noise(request, ni_set_idx):
    target_noise = get_object_or_404(Noise, ni_set_idx=ni_set_idx)
    data_set_idx = target_noise.data_set_idx.data_set_idx
    target_noise.delete()
    
    return redirect(reverse('rawsound:noise_info', args=[data_set_idx]))
# END: Sound Noise



# START: Sound Detail
def detail_info(request, data_set_idx):
    context = {}
    
    context['metadata'] = get_object_or_404(Metadata, data_set_idx=data_set_idx)
    
    detail_list = Detail.objects.filter(data_set_idx=data_set_idx)
    context['detail_list'] = detail_list
    
    return render(request, 'metadata/detail_info.html', context)


def create_detail(request, data_set_idx):
    Detail.objects.create(
        data_set_idx = get_object_or_404(Metadata, data_set_idx=data_set_idx),
        snd_info = request.POST.get('snd_info'),
        snd_cate = request.POST.get('snd_cate'),
        snd_sub_cate = request.POST.get('snd_sub_cate'),
        snd_cmnt = request.POST.get('snd_cmnt'),
        snd_place = request.POST.get('snd_place'),
        snd_ni_db = request.POST.get('snd_ni_db'),
        snd_ni_luf = request.POST.get('snd_ni_luf'),
        snd_srt_time = request.POST.get('snd_srt_time'),
        snd_end_time = request.POST.get('snd_end_time'),
        snd_device = request.POST.get('snd_device'),
    )
    
    return redirect(reverse('rawsound:detail_info', args=[data_set_idx]))


def update_detail(request, snd_set_idx):
    target_detail = get_object_or_404(Detail, snd_set_idx=snd_set_idx)
    target_detail.snd_info = request.POST.get('snd_info')
    target_detail.snd_cate = request.POST.get('snd_cate')
    target_detail.snd_sub_cate = request.POST.get('snd_sub_cate')
    target_detail.snd_cmnt = request.POST.get('snd_cmnt')
    target_detail.snd_place = request.POST.get('snd_place')
    target_detail.snd_ni_db = request.POST.get('snd_ni_db')
    target_detail.snd_ni_luf = request.POST.get('snd_ni_luf')
    target_detail.snd_srt_time = request.POST.get('snd_srt_time')
    target_detail.snd_end_time = request.POST.get('snd_end_time')
    target_detail.snd_device = request.POST.get('snd_device')
    target_detail.save()
    
    data_set_idx = target_detail.data_set_idx.data_set_idx
    
    return redirect(reverse('rawsound:detail_info', args=[data_set_idx]))


def delete_detail(request, snd_set_idx):
    target_detail = get_object_or_404(Detail, snd_set_idx=snd_set_idx)
    data_set_idx = target_detail.data_set_idx.data_set_idx
    target_detail.delete()
    
    return redirect(reverse('rawsound:detail_info', args=[data_set_idx]))
# END: Sound Detail



def generate_random_metadata():
    data_set = get_random_string(10)
    version = "version 240927"
    media_url = f"Test URL rawsound {get_random_string(5)}"
    ado_result = "test"
    bit_dep = 20240927
    rec_strime = "test"
    tdms_flag = "test"
    reg_user = "test"

    Metadata.objects.create(
        data_set=data_set,
        version=version,
        media_url=media_url,
        ado_result=ado_result,
        bit_dep=bit_dep,
        rec_strime=rec_strime,
        tdms_flag=tdms_flag,
        reg_user=reg_user,
    )