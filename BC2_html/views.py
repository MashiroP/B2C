import os

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect,render,HttpResponse
from django.conf.urls.static import static
from BC2_admin.models import profile
from BC2_html.form import Commodity_editor
from BC2_admin.models import commodity,category
import datetime
import random



def BC2_index(request):
    context={}
    context['goods']=commodity.objects.all()[0:9]
    return render(request,'BC2_html/index.html',context)


def BC2_login(request):
    return render(request, 'BC2_html/login.html')




def BC2_User(request):
    data={}
    if request.POST:
        email=request.POST.get('email')
        # 获取用户输入的邮箱 和  密码
        password=request.POST.get('password')
        active=User.objects.filter(email=email).first()
        # 判断邮箱是否 被注册
        if active:
            if active.is_active == False:
                # 判断用户邮箱密码是否正确
                
                data['ERRO'] = 3
                return JsonResponse(data)
            use = auth.authenticate(request, username=email, password=password)
            # 如果正确就把用户对象传入
            if use != None:
                # 传入然后对象 使用auth.login 进行登录
                auth.login(request, use)
                data['ERRO'] = 2
                return JsonResponse(data)
            else:
                #如果邮箱没有被注册则帮助用户注册
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
    contact_list = commodity.objects.all()
    paginator = Paginator(contact_list, 5)  # Show 25 contacts per page
    page = request.GET.get('page', 2)
    contacts = paginator.page(page)
    hq = contacts.number
    hq1 = list(range(max(hq - 2, 1), hq)) + list(range(hq, min(hq + 2, paginator.num_pages) + 1))
    contacts1 = {}
    contacts1['hq1'] = hq1
    contacts1['contacts'] = contacts
    contacts1['contact_list'] = contact_list
    return render(request,'sous.html',contacts1)







