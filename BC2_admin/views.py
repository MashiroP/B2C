import datetime
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import os
from django.shortcuts import redirect

import BC2_admin
from .models import *
from django.contrib.auth.models import User
from BC2_admin.models import profile, category, category_Subcategory


def test(USer_data,page=1):
    paginator = Paginator(USer_data, 10)
    
    """
    获取 用户数据 然后使用 Paginator分页器 每页10条数据
    
    paginator.page(page) 获取总共的数据
    
    page_number = list(range(max(number - 2, 5), number)) + list(range(number, min(number + 2, paginator.num_pages) + 1))
     获取获取页码的 前两页和后两页  使用max 和 min 在用list 变成列表 在列表拼接 传过前台
     
    """
    
    contacts = paginator.page(page)
    number = contacts.number
    page_number = list(range(max(number - 2, 5), number)) + list(
        range(number, min(number + 2, paginator.num_pages) + 1))
    contacts1 = { }
    contacts1 ['page_number'] = page_number
    contacts1 ['contacts'] = contacts
    return contacts1


def BC2_User_modify(request):
    
    uid = request.GET.get('uid')
    # 用户数据修改
    return render(request,'BC2_admin/BC2_User_modify.html',{'user':User.objects.get(id=uid)})

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

    return render(request,'BC2_admin/BC2_User_detailed.html',{'user':User.objects.get(id=request.GET.get('uid'))})

def dle_user(request):
    # 用户数据删除
    data = {}
    uid=request.GET.get('upid')
    print(uid)
    User.objects.get(id=uid).delete()
    data['erro']=1
    print(1)
    return JsonResponse(data)


def UP_user_data(request):
    # 用户数据修改上传
    if request.POST:
        user=User.objects.get(id=request.POST.get('user_id'))
        user.username=request.POST.get('username')
        user.email=request.POST.get('email')
        user.profile.sex=request.POST.get('sex')
        user.profile.state= request.POST.get('state')

        province=request.POST.get('P1')# 省
        city=request.POST.get('C1')# 市
        area=request.POST.get('A1')#  区
        address=request.POST.get('address')# 详细地址
        user.profile.Phone = request.POST.get('Phone')
        
        if province==city:
            user.profile.address = city+area+address
            user.profile.save( )
        #     拼接详细地址
        else:
            user.profile.address =province+ city + area + address
            user.profile.save()
        img = user.profile.headimage
        try:
            # 判断用户的头像是否是默认头像
            if str(img)== './static/media/img/1.jpg':
                pass
            else:
                os.remove(str(img))
                myfile = request.FILES.get("file", None)
                if myfile==None:
                    pass
                else:
                    name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
                    img = os.path.join('./static/media/img/' + name)
                    destination = open(img, 'wb+')
                    for i in myfile.chunks( ):
                        destination.write(i)
                    destination.close()
                
        except:
            user.save()
            user.profile.save()
        return redirect("BC2_admin_User")

def BC2_admin_User(request):
    paginator=User.objects.all().order_by("id")
    print(profile.objects.all())
    print(paginator)
        #  获取用户数据 然后根据ID继续进行排序
    contacts1 = test(paginator,request.GET.get('page', 1) )
    #     使用test 函数 获取 用户分页上数据
    
    
    if request.is_ajax():
        id = request.GET.get('uid')
        get_user = User.objects.get(id=id)
        return JsonResponse({})

    return render(request, 'BC2_admin/BC2_User.html', contacts1)

def search(request):
    
    search_data=request.GET.get('title')
    # 获取用户输入的 查询值
    
    city=request.GET.get('city')
    # 获取用户选择的查询的字段

    USer_data = User.objects.filter().order_by('id')
    # 简单的判断
    if request.GET.get('city') == 'name':
        USer_data =USer_data.filter(username__icontains=search_data)

    elif request.GET.get('city')== 'email':
        USer_data = USer_data.filter(email__icontains=search_data)

    elif request.GET.get('city')=='Phone':
        USer_data = USer_data.filter(profile__Phone__icontains=search_data)

    elif request.GET.get('city')=='sex':
        if request.GET.get('city')=='男':
            USer_data =USer_data.filter(profile__sex__icontains='1')
        else:
            USer_data =USer_data.filter(profile__sex__icontains='0')

    elif request.GET.get('city')=='state':
        
        if request.GET.get('city') == '活动':
            
            USer_data = USer_data.filter(profile__state__icontains= '1')
            
        else:
            
            USer_data = USer_data.filter(profile__state__icontains= '0')

    contacts1=test(USer_data,request.GET.get('page', 1))
    
    #     使用test 函数 获取 用户分页上数据
    
    return render(request, 'BC2_admin/BC2_User.html', contacts1)


def BC2_category(request):
    context={}
    gory=category.objects.all()
    
    context['gory']=gory
    if request.POST:
        print(request.POST)
        cate = request.POST.get('category')
        Subca = request.POST.get('Subcategory')

        try:
            if request.POST.get('hiud')=='2':
                category.objects.create(category_father=Subca)
            else:
                cat=category.objects.get(id=cate)
                Subcat = category_Subcategory()
                Subcat.Subgrade_name = Subca
                Subcat.uid = cat
                Subcat.save()
            
        except:
            pass
        else:
            return  JsonResponse({'data':"ok"})
    return  render(request,'BC2_admin/BC2_category.html',context)

def BC2_View_category(request):
    context = { }
    gory = category_Subcategory.objects.all()
    context ['gory'] = gory
    if request.is_ajax():
        try:
            if request.GET.get('del'):
                category_Subcategory.objects.get(id=request.GET.get('upid')).delete()
                return JsonResponse({ "msg": '2' })
        except:
            return JsonResponse({ "msg": '3' })
        up_category=category_Subcategory.objects.get(id=request.GET.get('upid'))
        up_category.Subgrade_name=request.GET.get('title')
        up_category.save()
        return JsonResponse({"msg":'1'})
    return render(request,'BC2_admin/BC2_View_category.html', context)
    


