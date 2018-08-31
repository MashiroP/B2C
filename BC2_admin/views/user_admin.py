import datetime
from django.contrib import auth
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
import os
from django.contrib.auth.models import User
from BC2_admin.models import profile, category, category_Subcategory, commodity
from django.contrib.auth.hashers import make_password, check_password
from ..extend.page import test


def admin_login (request):
	if request.POST and request.session.get('verifycode').upper( ) == request.POST.get('vcod').upper( ):
		
		name = request.POST.get('name')
		password = request.POST.get('Password')
		use = auth.authenticate(request, username=name, password=password)
		# 如果正确就把用户对象传入
		if use != None:
			request.session ['AdminUser'] = { 'username': use.username }
			auth.login(request, use)
			return redirect('Backstage')
	return render(request, 'BC2_admin/login.html')


from PIL import Image, ImageDraw, ImageFont


def verifycode (request):
	# 引入绘图模块
	
	# 引入随机函数模块
	import random
	# 定义变量，用于画面的背景色、宽、高
	bgcolor = (random.randrange(20, 100), random.randrange(
		20, 100), 255)
	width = 100
	height = 25
	# 创建画面对象
	im = Image.new('RGB', (width, height), bgcolor)
	# 创建画笔对象
	draw = ImageDraw.Draw(im)
	# 调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		draw.point(xy, fill=fill)
	# 定义验证码的备选值
	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	# str1 = '123456789'
	# 随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str1 [random.randrange(0, len(str1))]
	# 构造字体对象
	font = ImageFont.truetype('fonts-japanese-mincho.ttf', 23)
	# 构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	# 绘制4个字
	draw.text((5, 2), rand_str [0], font=font, fill=fontcolor)
	draw.text((25, 2), rand_str [1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str [2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str [3], font=font, fill=fontcolor)
	# 释放画笔
	del draw
	# 存入session，用于做进一步验证
	request.session ['verifycode'] = rand_str
	# 内存文件操作
	import io
	buf = io.BytesIO( )
	# 将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	# 将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue( ), 'image/png')
def Backstage (request: object):
	return render(request, 'Backstage.html')


def User_modify (request):
	uid = request.GET.get('uid')
	# 用户数据修改
	return render(request, 'BC2_admin/User/User_modify.html', { 'user': profile.objects.get(id=uid) })


def User_is_active (request):
	user = User.objects.get(id=request.GET.get('User_Id'))
	if user.is_active:
		user.is_active = False
	else:
		user.is_active = True
	user.save( )
	return JsonResponse({ 'bcak': 1 })


def User_detailed (request):
	return render(request, 'BC2_admin/User/User_detailed.html', { 'user': profile.objects.get(id=request.GET.get('uid')) })


def User_dle (request):
	data = { }
	uid = request.GET.get('upid')
	profile.objects.get(id=uid).delete()
	data ['erro'] = 1
	return JsonResponse({ 'bcak': 1 })


from ..extend.upfile import file


def UP_user_data (request):
	# 用户数据修改上传
	if request.POST:
		user = profile.objects.get(id=request.POST.get('user_id'))
		user.user = request.POST.get('username')
		user.email = request.POST.get('email')
		user.active = request.POST.get('state')
		user.sex = request.POST.get('sex')
		user.Phone = request.POST.get('Phone')
		myfile = request.FILES.get("file", None)

		img = user.headimage
		if img=='./static/media/img/1.jpg':
			pass
		else:
			if os.path.exists(str(img)) and myfile:
				os.remove(str(img))
		if myfile:
			name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
			img = os.path.join('./static/media/img/' + name)
			file(img, myfile)
			user.headimage = img
		user.save( )
		return redirect('User_list')


def User_list (request):
	paginator = profile.objects.all( ).order_by("id")
	#  获取用户数据 然后根据ID继续进行排序
	contacts1 = test(paginator, request.GET.get('page', 1))
	#     使用test 函数 获取 用户分页上数据
	if request.is_ajax( ):
		id = request.GET.get('uid')
		get_user = profile.objects.get(id=id)
		return JsonResponse({ })
	
	return render(request, 'BC2_admin/User/User_list.html', contacts1)


def User_search (request):
	search_data = request.GET.get('title')
	# 获取用户输入的 查询值
	
	city = request.GET.get('city')
	# 获取用户选择的查询的字段
	
	USer_data = profile.objects.filter( ).order_by('id')
	# 简单的判断
	if request.GET.get('city') == 'name':
		USer_data = USer_data.filter(user__icontains=search_data)
	
	elif request.GET.get('city') == 'email':
		USer_data = USer_data.filter(email__icontains=search_data)
	
	elif request.GET.get('city') == 'Phone':
		USer_data = USer_data.filter(Phone__icontains=search_data)
	
	elif request.GET.get('city') == 'sex':
		if request.GET.get('city') == '男':
			USer_data = USer_data.filter(sex__icontains='1')
		else:
			USer_data = USer_data.filter(sex__icontains='0')
	
	elif request.GET.get('city') == 'state':
		
		if request.GET.get('city') == '活动':
			
			USer_data = USer_data.filter(active__icontains=True)
		else:
			USer_data = USer_data.filter(active__icontains=False)
	page=request.GET.get('page', 1)
	if int(page)!=1:
		page=1
	contacts1 = test(USer_data, page)
	return render(request, 'BC2_admin/User/User_list.html', contacts1)


def User_add(request):
	if request.POST:
		user = profile()
		user.user = request.POST.get('username')
		user.email = request.POST.get('email')
		user.sex = request.POST.get('sex')
		user.Phone =request.POST.get('Phone')
		user.password=make_password(request.POST.get('password'),'pbkdf_sha256')
		myfile = request.FILES.get("file", None)
		if myfile:
			name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
			img = os.path.join('./static/media/img/' + name)
			file(img, myfile)
			user.headimage = img
		user.save()
		return redirect('User_list')
	return render(request, 'BC2_admin/User/User_add.html')

