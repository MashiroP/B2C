import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import os
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User
from user.models import profile


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
    # 用户数据删除
    data = {}
    uid=request.GET.get('upid')
    print(uid)
    profile.objects.get(id=uid).delete()
    data['erro']=1
    print(1)
    return JsonResponse(data)



def UP_user_data(request):
    # 用户数据修改上传
    if request.POST:
        user=profile.objects.get(id=request.POST.get('user_id'))
        user.user=request.POST.get('username')
        user.email=request.POST.get('email')
        user.sex=request.POST.get('sex')
        user.state= request.POST.get('state')

        province=request.POST.get('P1')# 省
        city=request.POST.get('C1')# 市
        area=request.POST.get('A1')#  区
        address=request.POST.get('address')# 详细地址
        user.Phone = request.POST.get('Phone')
        
        if province==city:
            user.address =city+area+address
        #     拼接详细地址
        else:
            user.address =province+ city + area + address
        img = user.headimage
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
            pass
        user.save()
        return redirect("BC2_admin_User")

def BC2_admin_User(request):
    paginator=profile.objects.all().order_by("id")
        #  获取用户数据 然后根据ID继续进行排序
    contacts1 = test(paginator,request.GET.get('page', 1) )
    #     使用test 函数 获取 用户分页上数据
    
    
    if request.is_ajax():
        id = request.GET.get('uid')
        get_user = profile.objects.get(id=id)
        return JsonResponse({})

    return render(request, 'BC2_admin/BC2_User.html', contacts1)








def search(request):
    
    search_data=request.GET.get('title')
    # 获取用户输入的 查询值
    
    city=request.GET.get('city')
    # 获取用户选择的查询的字段

    USer_data = profile.objects.filter().order_by('id')
    # 简单的判断
    if request.GET.get('city') == 'name':
        USer_data =USer_data.filter(user__icontains=search_data)

    elif request.GET.get('city')== 'email':
        USer_data = USer_data.filter(email__icontains=search_data)

    elif request.GET.get('city')=='Phone':
        USer_data = USer_data.filter(Phone__icontains=search_data)

    elif request.GET.get('city')=='sex':
        if request.GET.get('city')=='男':
            USer_data =USer_data.filter(sex__icontains='1')
        else:
            USer_data =USer_data.filter(sex__icontains='0')

    elif request.GET.get('city')=='state':
        
        if request.GET.get('city') == '活动':
            
            USer_data = USer_data.filter(state__icontains= '1')
            
        else:
            
            USer_data = USer_data.filter(state__icontains= '0')

    contacts1=test(USer_data,request.GET.get('page', 1))
    
    #     使用test 函数 获取 用户分页上数据
    
    return render(request, 'BC2_admin/BC2_User.html', contacts1)
from django.contrib.auth import authenticate, login
from .email_Backend import EmailBackend
def user_test(request):
    data=request.GET
    print(data)
    user = EmailBackend()
    user.authenticate(request=request, **data)
    if user == None :
        print(1)
    else:
        print(2)
    return render(request, 'BC2_admin/test.html')
# 验证失败