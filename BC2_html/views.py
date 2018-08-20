import os

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render,HttpResponse
from django.conf.urls.static import static

from BC2_html.form import Commodity_editor
from user import models
from .models import commodity,category
import datetime
import random



def BC2_index(request):
    context={}
    context['goods']=commodity.objects.all()
    return render(request,'BC2_html/index.html',context)


def BC2_login(request):
    return render(request, 'BC2_html/login.html')




def BC2_User(request):
    data={}
    if request.POST:
        email=request.POST.get('email')
        password=request.POST.get('password')
        active=User.objects.filter(email=email).first()
        if active:
            if active.is_active == False:
                data['ERRO'] = 3
                return JsonResponse(data)
            use = auth.authenticate(request, username=email, password=password)
            if use != None:
                auth.login(request, use)
                data['ERRO'] = 2
                return JsonResponse(data)
            else:
                try:
                    user_data = User.objects.create_user(username=email, password=password, is_active=True, email=email)
                except :
                    data['ERRO'] = 1
                    return JsonResponse(data)
        else:
            user_data = User.objects.create_user(username=email, password=password, is_active=True, email=email)
            user_data.save()
            auth.login(request, user_data)
            data['ERRO'] = 2
            return JsonResponse(data)


def test(request):
    context={}
    context['User']=User.objects.all()
    context['category'] = category.objects.all()

    return render(request, 'test.html',context)


def BC2_admin_index(request):

    context={}
    context['category']=category.objects.all()
    Writeblog=Commodity_editor()
    context['from'] = Writeblog
    return render(request, 'BC2_admin/index.html', context)


def BC2_admin_User(request):
    context={}
    context['User']=User.objects.all()
    return render(request, 'BC2_admin/BC2_User.html', context)


def upload_data(request):
    context = {}
    myfile = request.FILES.get("Commodity_img", None)
    name=str(datetime.datetime.now())+'_'+str(request.FILES.get('Commodity_img'))
    img=os.path.join('./static/media/goods/'+name)
    destination = open(img, 'wb+')
    for i in myfile.chunks():
        destination.write(i)
    destination.close()
    data=request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    data.pop('Commodity_category')
    data['Commodity_img']=img
    commo=commodity.objects.create(**data)

    ts = category.objects.get(id=request.POST.get('Commodity_category'))

    commo.Commodity_category.add(ts)

    return redirect('/')


def commodity_list(request,uid):
    context={}

    bt=category.objects.get(id=uid)

    context['commodity'] = bt.commodity_set.all()
    return render(request, 'BC2_admin/commodity.html', context)


def sous(request):
    return render(request,'sous.html')