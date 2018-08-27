import os
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect,render,HttpResponse
from BC2_html.form import Commodity_editor
from BC2_admin.models import commodity,category,category_Subcategory,profile
import datetime
import random
from BC2_admin.extend.page import test as te

from BC2_html.extend.damo import a


def BC2_index(request):
    context=a()
    context['goods']=commodity.objects.all()[0:9]
    return render(request,'BC2_html/index.html',context)

def login(request):
    data = {}
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(email) == 11 and str(email).isdigit( ):
            # 获取用户输入的邮箱 和  密码
            use = auth.authenticate(request, username=email, password=password)
            # 如果正确就把用户对象传入
            if use != None:
                # 传入然后对象 使用auth.login 进行登录
                auth.login(request, use)
                data ['ERRO'] = 2
                return JsonResponse(data)
            else:
                data ['ERRO'] = 1
                return JsonResponse(data)
    return render(request, 'BC2_html/login.html')


def BC2_User(request):
    data={}
    if request.POST:
        email=request.POST.get('email')
        password = request.POST.get('password')
        if len(email) == 11 and str(email).isdigit():
            user_data = User.objects.create_user(username=email, password=password, is_active=True,)
            auth.login(request, user_data)
            data['ERRO'] = 2
            return JsonResponse(data)
        else:
            data ['ERRO'] = 3
            return JsonResponse(data)
    else:
        return  render(request,'BC2_html/zc.html')
    
#     注销登录
def userLogout(request):
    auth.logout(request)
    return redirect('/')
    





def BC2_admin_index(request):

    context={}
    context['category']=category_Subcategory.objects.all()
    Writeblog=Commodity_editor()
    context['from'] = Writeblog
    return render(request, 'BC2_admin/index.html', context)


def create(request):
    return render(request,'BC2_html/create.html')

def up_User(request):
    use=User.objects.get(id=request.GET.get('id'))

    return render(request, 'BC2_html/blog.html')

def dxyzm (content,phone):
    import urllib
    import urllib.request
    import hashlib

    def md5 (str):
        import hashlib
        m = hashlib.md5( )
        m.update(str.encode("utf8"))
        return m.hexdigest( )

    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词',
        '51':'短信发送成功',
    }

    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = '643813251'
    # 短信平台密码
    password = md5('643813251')
    # 要发送的短信内容
    data = urllib.parse.urlencode({ 'u': user, 'p': password, 'm': phone, 'c': content })
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read( ).decode('utf-8')
    return statusStr [the_page]

def dxyz(request):
    return render(request, 'BC2_html/phone_cick.html')
def dx(request):
    key = request.POST.get('key')
    phone = request.POST.get('phone')

    if int(key) ==request.session.get('key', default=None):
        use = User.objects.get(username=phone)
        use=profile.objects.get(id=use.profile.id)
        use.active=1
        use.save()

        return redirect('/')
    else:
        return render(request, 'BC2_html/phone_cick.html',{'msg':'验证码错误'} )



def yzmfs(request):
    phone = request.GET.get('upid')
    yzm = random.randrange(1111, 9999)
    request.session ['key'] = yzm
    request.session.set_expiry(600)
    content = '你的验证码是%s,有效时间为10分钟' % (yzm)

    res = dxyzm(content=content, phone=phone)
    return  JsonResponse({ 'ERRO':1})

def catalog_list(request):
    Uid=request.GET.get('cat_fid',1)
    cont=category.objects.get(id=Uid)
    paginator =cont.category_subcategory_set.filter().order_by('-id')
    contacts1 = te(paginator, request.GET.get('page', 1))
    contacts1 ['category'] = category.objects.all()
    for i in contacts1 ['category']:
        contacts1 ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
   
    return render(request, 'BC2_html/catalog_list.html',contacts1)


def catalog_lists (request):
    cat_Sid = request.GET.get('cat_Sid', None)
    print(cat_Sid)
    if cat_Sid:
        cont = category_Subcategory.objects.get(id=cat_Sid)
        paginator=cont.commodity_set.all()
        print(paginator)
    contacts1 = te(paginator, request.GET.get('page', 1))
    contacts1 ['category'] = category.objects.all( )
    for i in contacts1 ['category']:
        contacts1 ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
    return render(request, 'BC2_html/lists.html', contacts1)


def commod(request,Uid):
    context = a()
    context['commo']=commodity.objects.get(id=Uid)

    
    return render(request, 'BC2_html/product_page.html',context)