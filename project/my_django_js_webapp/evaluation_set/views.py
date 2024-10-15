from django.shortcuts import render
from sound.models import Metadata, Detail, Noise
from django.http import Http404, HttpResponse, JsonResponse

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