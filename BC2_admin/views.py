import datetime
from django.contrib import auth
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
import os
from django.contrib.auth.models import User
from BC2_admin.models import profile, category, category_Subcategory, commodity
from BC2_html.form import Commodity_editor
from .extend.page import test



def Backstage(request: object):
    return render(request, 'test.html')


def BC2_User_modify(request):
    uid = request.GET.get('uid')
    # 用户数据修改
    return render(request,'BC2_admin/BC2_User_modify.html',{'user':User.objects.get(id=uid)})

def User_is_active(request):
    user=User.objects.get(id=request.GET.get('User_Id'))
    if user.is_active:
        user.is_active=False
    else:
        user.is_active=True
    user.save()
    return JsonResponse({'bcak':1})

def BC2_User_detailed(request):
    return render(request,'BC2_admin/BC2_User_detailed.html',{'user':User.objects.get(id=request.GET.get('uid'))})

def dle_user(request):
    data = {}
    uid=request.GET.get('upid')
    User.objects.get(id=uid).delete()
    data['erro']=1
    return JsonResponse({'bcak':1})
from .extend.upfile import file

def UP_user_data(request):
    # 用户数据修改上传
    if request.POST:
        user=User.objects.get(id=request.POST.get('user_id'))
        user.username=request.POST.get('username')
        user.email=request.POST.get('email')
        user.is_active = request.POST.get('state')
        province = request.POST.get('P1')  # 省
        city = request.POST.get('C1')  # 市
        area = request.POST.get('A1')  # 区
        address = request.POST.get('address')  # 详细地址
        use_s=profile.objects.get(name_id=user)
        use_s.sex=request.POST.get('sex')
        use_s.Phone = request.POST.get('Phone')
        myfile = request.FILES.get("file", None)
        if province==city:
            use_s.address = city+area+address
        #     拼接详细地址
        else:
            use_s.address =province+ city + area + address
        img = use_s.headimage
        if os.path.exists(str(img)) and myfile:
            os.remove(str(img))
        else:
            pass
       
        if myfile:
            name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
            img = os.path.join('./static/media/img/' + name)
            file(img, myfile)
            use_s.headimage = img
        user.save()
        use_s.save()
        if user.is_superuser:
            return  redirect('BC2_admin_User')
        else:
            return redirect('create')

def BC2_admin_User(request):
    paginator=User.objects.all().order_by("id")
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
    context = {}
    gory = category_Subcategory.objects.all()

    paginator = gory.order_by("uid_id")
    #  获取用户数据 然后根据ID继续进行排序
    contacts1 = test(paginator, request.GET.get('page', 1))
    
    context ['gory'] = contacts1
    if request.is_ajax():
        try:
            if request.GET.get('del'):
                
                a=category_Subcategory.objects.get(id=request.GET.get('upid'))
                print(bool(a.commodity_set.all()))
                if bool(a.commodity_set.all()):
                    return JsonResponse({ "msg": '1' })
                else:
                    category_Subcategory.objects.get(id=request.GET.get('upid')).delete()
                    return JsonResponse({ "msg": '2' })
        except:
            return JsonResponse({ "msg": '3' })
        up_category=category_Subcategory.objects.get(id=request.GET.get('upid'))
        up_category.Subgrade_name=request.GET.get('title')
        up_category.save()
        return JsonResponse({"msg":'1'})
    return render(request,'BC2_admin/BC2_View_category.html', contacts1)
    


def upload_data(request):
    context = {}
    myfile = request.FILES.get("file", None)
    name=str(datetime.datetime.now())+'_'+str(request.FILES.get('file'))
    img=os.path.join('./static/media/goods/'+name)
    file(img, myfile)
    data=request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    data['Commodity_img']=img
    data['uid']=category_Subcategory.objects.get(id=data['Commodity_category'])
    data.pop('Commodity_category')
    commo=commodity.objects.create(**data)
    return redirect('/')


def commodity_list(request):
    city = request.GET.get('city')
    search_data = request.GET.get('search')
    data = commodity.objects.filter().order_by('id')
    # 简单的判断
    if city =='Texture':
        data=data.filter(uid__Subgrade_name__icontains=search_data)
    elif city =='title':
        data = data.filter(uid__Subgrade_name__icontains=search_data)
    paginator = data.order_by("id")
    contacts1 = test(paginator, request.GET.get('page', 1))
    contacts1 ['gory'] = contacts1
    return render(request, 'BC2_admin/commodity.html', contacts1)


def commodity_state(request):
    context = {}
    upid=request.GET.get('uid')
    
    comm = commodity.objects.get(id=upid)
    context['comm']=commodity.objects.get(id=upid)
    Writeblog=Commodity_editor()
    context['from'] = Writeblog
    context['cate']=category_Subcategory.objects.all()
    return render(request,'BC2_admin/commodity_state.html',context)


def commodity_seve(request):
    if request.POST:
        comm=commodity.objects.get(id=request.POST.get('upid'))
        data = request.POST.dict( )
        myfile = request.FILES.get("file", None)
        if myfile != None:
            name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
            img = os.path.join('./static/media/goods/' + name)
            destination = open(img, 'wb+')
            for i in myfile.chunks( ):
                destination.write(i)
            destination.close( )
            comm.Commodity_img = img
        comm.Commodity_name = data['Commodity_name']
        comm.Price = data['Price']
        comm.state = data['state']
        comm.Stock=data['Stock']
        comm.describe=data['describe']
        comm.uid=category_Subcategory.objects.get(id=data['Commodity_category'])
        comm.save()
    return redirect('/BC2_admin/BC2_admin_commodity')




def img_get(request):
    date_path = datetime.datetime.now().strftime('%Y/%m/%d')
    myfile = request.FILES.get("file", None)
    name =str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
    img = os.path.join('./static/media/goods/'+ name)
    destination = open(img, 'wb+')
    for i in myfile.chunks( ):
        destination.write(i)
    destination.close()
    return JsonResponse( {"location":img})


def admin_login(request):

    if request.POST and request.session.get('verifycode').upper()==request.POST.get('vcod').upper():
    
        name = request.POST.get('name')
        password = request.POST.get('Password')
        use = auth.authenticate(request, username=name, password=password)
        # 如果正确就把用户对象传入
        if use != None:
            auth.login(request, use)
            return redirect('Backstage')
    return render(request, 'BC2_admin/login.html')

from PIL import Image,ImageDraw,ImageFont

def verifycode(request):
    #引入绘图模块
 
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('fonts-japanese-mincho.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


