# -*- coding:utf-8 -*-
# coding:utf-8
import json
import os
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect,render,HttpResponse
from django.urls import reverse
from BC2_admin.models import commodity, category, category_Subcategory, profile, Address, Order, OrderInfo
from BC2_admin.models import cart as Cart_s
import datetime
import random
from BC2_admin.extend.page import test as te
from BC2_html.extend.damo import a,dxyzm
from django.contrib.auth.hashers import make_password, check_password




def index(request):
    context=a()
    context['goods']=commodity.objects.all()[0:4]
    return render(request,'BC2_html/index.html',context)




import codecs

def login(request):
    nextpath = request.GET.get('nextpath')
    url=request.GET.get('url')
    if request.POST:
        
        user=profile.objects.get(Phone=str(request.POST.get('Phone')))
        password=request.POST.get('password')
        if check_password(password,user.password):
            request.session ['User'] = { 'uid': user.id, 'user': user.user, 'Phone': user.Phone }
            bcak='location.href ="%s"'%(nextpath)
            

          

            return HttpResponseRedirect(nextpath)
        
            
    return render(request, 'BC2_html/login.html')


def SMS(request):
    phone = request.GET.get('Phone')
    if len(phone) == 11 and str(phone).isdigit():
        rand=random.randrange(1111, 9999)
        request.session ['SMS'] =rand
        request.session.set_expiry(600)
        content = '你的验证码是%s,有效时间为10分钟' % (rand)
        res = dxyzm(content=content, phone=phone)
        return  JsonResponse({ 'error':rand})
    else:
        return JsonResponse({ 'error': '2' })
        
    





def register(request):
    data={}
    if request.POST:
        sms=request.session.get('SMS')
        vcod = request.POST.get('vcod')
        if int(vcod)==int(sms):
            email=request.POST.get('email')
            name = request.POST.get('user')
            password = request.POST.get('password')
            Phone=request.POST.get('Phone')
            sex=request.POST.get('sex')
            password=make_password(password)
            user=profile.objects.create(
                user=name,
                email=email,
                Phone=Phone,
                sex=sex,
                password=password
            )
            return redirect('login')
        else:
            return HttpResponse('<script>alert("验证码错误");javascript:history.go(-1);</script>')
    return render(request, 'BC2_html/register.html')


#     注销登录
def userLogout(request):
    auth.logout(request)
    return redirect('/')


def create(request):
    context = a( )
    return render(request,'BC2_html/create.html',context)

def up_User(request):
    context = a()
    use=User.objects.get(id=request.GET.get('id'))

    return render(request, 'BC2_html/blog.html',context)



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

    if cat_Sid:
        cont = category_Subcategory.objects.get(id=cat_Sid)
        paginator=cont.commodity_set.all()

    contacts1 = te(paginator, request.GET.get('page', 1))
    contacts1 ['category'] = category.objects.all( )
    for i in contacts1 ['category']:
        contacts1 ['category_Subcategory'] = category_Subcategory.objects.filter(uid=i.id)
    return render(request, 'BC2_html/lists.html', contacts1)


def commod(request,Uid):
    context = a()
    commo=commodity.objects.get(id=Uid)
    context['commo']=commo
    commo.Clicks+=1
    commo.save()
    return render(request, 'BC2_html/product_page.html',context)


def addcart(request):
    gid = request.GET.get('gid')
    num = int(request.GET.get('num'))
 

    # 在session中获取购物车数据
    data = request.session.get('cart',{})

    # 判断要加入到购物车的商品,是否已经存在
    if data.get(gid):
        # 商品已经存在,修改数量
        data[gid]['num'] += num
    else:
        # 如果不存在,则把商品添加到购物车中
        # 把要添加的商品加入到购物车数据中
        data[gid] = {'gid':gid,'num':num}
    
    # 把配置号的购物车数据,再存入到session
    request.session['cart'] =data


    # 返回json
    return JsonResponse({'error':0,'msg':'加入购物车成功'})




def cart(request):
    context = a()
    if request.session.get('cart', {}):
        data = request.session ['cart']
        user=request.session.get('User', {})
        if user:
            aa = profile.objects.get(id=user.get('uid'))
            for i in aa.cart_set.all():
                data [i.goos_id.id] = { 'gid': i.goos_id.id, 'num': i.num }
        for k, i in data.items( ):
            data [k] ['goods'] = commodity.objects.get(id=k)
        context ['data'] = data
    return render(request, 'BC2_html/shopping_cart.html',context)

def cart_del(request):
    data = request.session ['cart']
    gid=request.GET.get('gid')
    zhi=request.GET.get('zhi')
    data.get(str(gid))['num']=zhi
    request.session ['cart']=data
    return JsonResponse({})

def cart_sc(request):
    return JsonResponse({})


def ddsc(request):
    context = a()
    uid=request.session.get('User').get('uid',None)
    if uid:
        context['user']=profile.objects.get(id=uid)
    data=request.GET.get('gid')
    if bool(data):
        dictinfo = json.loads(data)
        b={}
        for i, v in dictinfo.items():
            gods = commodity.objects.get(id=i)
            b[gods] =v[1]
        context['gods']=b
        request.session ['order'] = data
    return render(request, 'BC2_html/ddym.html', context)

def address(request):
    if request.POST:
        data = request.POST.dict()
        if data.get('isstatus'):
            usdr_add=Address.objects.filter(uid=data.get('uid_id'))
            for i in usdr_add:
                i.isstatus=False
                i.save()
        data.pop('csrfmiddlewaretoken')
        Address.objects.create(**data)
        
    return render(request, 'BC2_html/addaddress.html')
# Order
def place_order(request):
    if request.POST:
        data = request.session.get('order', {})
        Data=request.session.get('order', {})
        data = json.loads(data)
        Data = json.loads(Data)
        address=request.POST.get('Address')
        Addre=Address.objects.get(id=address)
        user = User.objects.get(id=request.session.get('user_id'))
        order=Order()
        order.user_id=user
        order.Consignee=Addre.aname
        order.Receiving_address=Addre.ads
        order.phone=Addre.aphone
        order.Amount=0
        order.state=0
        order.save()
        num=0
        for i,v in Data.items():
            gods = commodity.objects.get(id=i)
            OrdIn=OrderInfo()
            OrdIn.orderid=order
            OrdIn.gid=gods
            OrdIn.num=int(v[1])
            OrdIn.price=int(v [1]) * int(gods.Price)
            OrdIn.save( )
            num+=(int(v[1])*int(gods.Price))
            Cart_s.objects.filter(goos_id=gods).delete()
            data.pop(i)
        order.Amount = num
        order.save()
        request.session ['cart'] = data
        return render(request, 'BC2_html/addaddress.html')
def test(request):
    a=reverse('login')
    a+='?a=1'
    return  redirect(a)


def Personal_Center(request):
    return render(request, 'BC2_html/Personal_Center.html')