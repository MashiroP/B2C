import datetime

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from gevent import os

from .models import *
from django.contrib.auth.models import User
from user.models import profile
def BC2_User_modify(request):
    if request.POST:
        # def upload_data(request):
        #     context = {}
            # myfile = request.FILES.get("Commodity_img", None)
            # name = str(datetime.datetime.now()) + '_' + str(request.FILES.get('Commodity_img'))
            # img = os.path.join('./static/media/goods/' + name)
            # destination = open(img, 'wb+')
            # for i in myfile.chunks():
            #     destination.write(i)
            # destination.close()
            # data = request.POST.dict()
            # data.pop('csrfmiddlewaretoken')
            # data.pop('Commodity_category')
            # data['Commodity_img'] = img
        print(1)
        print(request.POST)
        return render(request, 'BC2_admin/BC2_User_modify.html')
    uid = request.GET.get('uid')
    return render(request,'BC2_admin/BC2_User_modify.html',{'user':profile.objects.get(id=uid)})






def User_is_active(request):
    data={}
    data['1']=1
    user=User.objects.get(id=request.GET.get('User_Id'))

    if user.is_active:
        user.is_active=False
    else:
        user.is_active=True
    user.save()



    return JsonResponse(data)

def BC2_User_detailed(request):

    return render(request,'BC2_admin/BC2_User_detailed.html',{'user':profile.objects.get(id=request.GET.get('uid'))})



def dle_user(request):
    data = {}
    uid=request.GET.get('upid')
    print(uid)
    profile.objects.get(id=uid).delete()
    data['erro']=1
    print(1)
    return JsonResponse(data)



