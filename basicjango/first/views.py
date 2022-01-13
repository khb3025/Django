from django import template
from django.shortcuts import render
from django.http import HttpResponse
import random
#from django.template import loader
from datetime import datetime
# Create your views here.
def index(request):
    #template = loader.get_template('index.html')
    now = datetime.now()
    context ={"current_date" : now}
    #return HttpResponse(template.render(context, request))
    return render(request, 'first/index.html' , context)

def select(request):
    context={}
    #message = '수 하나를 입력해주세요.'
    #return HttpResponse(message)
    return render( request ,'first/select.html', context)

def result(request):
    chosen = int(request.GET['number'])
    
    results =[]
    if chosen >=1 and chosen <=56:
        results.append(chosen)
    
    box = []
    for i in range(0,45):
        if chosen != i+1:
            box.append(i+1)
    
    random.shuffle(box)
    for i in range(0,5):
        results.append(box.pop())
        
    context ={
        'numbers' : results
    }
    return render( request ,'first/result.html', context)

'''
def result(request, year):
    #message = '추첨 결과입니다.'
    #return HttpResponse(message) 
    context ={}
    return render( request ,'result.html', context)
'''