import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import os
from django.contrib.auth.models import User
from BC2_admin.extend.upfile import file
from BC2_admin.models import profile, category, category_Subcategory, commodity
from BC2_admin.form import Commodity_editor
from ..extend.page import test


def sort_add (request):
	context = {}
	gory = category.objects.all()
	context ['gory'] = gory
	if request.POST:
		cate = request.POST.get('category')
		Subca = request.POST.get('Subcategory')
		
		try:
			if request.POST.get('hiud') == '2':
				category.objects.create(category_father=Subca)
			else:
				cat = category.objects.get(id=cate)
				Subcat = category_Subcategory( )
				Subcat.Subgrade_name = Subca
				Subcat.uid = cat
				Subcat.save()
		except:
			pass
		else:
			return JsonResponse({ 'data': "ok" })
	return render(request, 'BC2_admin/management/sort_add.html', context)


def sort_View (request):
	context = { }
	gory = category_Subcategory.objects.all( )
	
	paginator = gory.order_by("uid_id")
	#  获取用户数据 然后根据ID继续进行排序
	contacts1 = test(paginator, request.GET.get('page', 1))
	
	context ['gory'] = contacts1
	if request.is_ajax( ):
		try:
			if request.GET.get('del'):
				
				a = category_Subcategory.objects.get(id=request.GET.get('upid'))
				print(bool(a.commodity_set.all( )))
				if bool(a.commodity_set.all( )):
					return JsonResponse({ "msg": '1' })
				else:
					category_Subcategory.objects.get(id=request.GET.get('upid')).delete( )
					return JsonResponse({ "msg": '2' })
		except:
			return JsonResponse({ "msg": '3' })
		up_category = category_Subcategory.objects.get(id=request.GET.get('upid'))
		up_category.Subgrade_name = request.GET.get('title')
		up_category.save( )
		return JsonResponse({ "msg": '1' })
	return render(request, 'BC2_admin/management/sort_View.html', contacts1)


def merchandise_add_data (request):
	context = { }
	
	myfile = request.FILES.get("file", None)
	if myfile:
		name = str(datetime.datetime.now( )) + '_' + str(request.FILES.get('file'))
		img = os.path.join('./static/media/goods/' + name)
		file(img, myfile)
	data = request.POST.dict()
	commo = commodity()
	commo.Commodity_name=data['name']
	commo.Price=data['Price']
	commo.uid=category_Subcategory.objects.get(id=data['uid'])
	commo.Stock=data['Stock']
	commo.state=data['state']
	commo.Commodity_img=img
	commo.save()
	
	
	return redirect('merchandise_list')


def merchandise_list (request):
	city = request.GET.get('city')
	search_data = request.GET.get('search')
	data = commodity.objects.filter( ).order_by('id')
	# 简单的判断
	if city == 'Texture':
		data = data.filter(uid__Subgrade_name__icontains=search_data)
	elif city == 'title':
		data = data.filter(uid__Subgrade_name__icontains=search_data)
	paginator = data.order_by("id")
	
	page=request.GET.get('page', 1)
	if int(page)!=1:
		page=1
	contacts1 = test(paginator,page)
	contacts1 ['gory'] = contacts1
	return render(request, 'BC2_admin/management/merchandise_list.html', contacts1)


def merchandise_edit (request):
	context = { }
	upid = request.GET.get('uid')
	
	comm = commodity.objects.get(id=upid)
	context ['comm'] = commodity.objects.get(id=upid)
	Writeblog = Commodity_editor( )
	context ['from'] = Writeblog
	context ['cate'] = category_Subcategory.objects.all( )
	return render(request, 'BC2_admin/management/merchandise_edit.html', context)


def merchandise_seve(request):
	if request.POST:
		comm = commodity.objects.get(id=request.POST.get('upid'))
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
		comm.Commodity_name = data ['Commodity_name']
		comm.Price = data ['Price']
		comm.state = data ['state']
		comm.Stock = data ['Stock']
		comm.describe = data ['describe']
		comm.uid = category_Subcategory.objects.get(id=data ['Commodity_category'])
		comm.save( )
	return redirect('comm_list')



def merchandise_state(request):
	uid=request.GET.get('uid')
	goods=commodity.objects.get(id=uid)
	
	
	if int(goods.state)!=2:
		goods.state=2
		goods.save()
	else:
		goods.state=1
		goods.save()
	return redirect('merchandise_list')

def merchandise_add(request):
    context={}
    context['category']=category_Subcategory.objects.all()
    Writeblog=Commodity_editor()
    context['from'] = Writeblog
    return render(request, 'BC2_admin/management/merchandise_add.html', context)