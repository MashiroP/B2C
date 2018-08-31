import re

from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import permission_required
from ..extend.page import test

def add_admin(request):
	if request.POST:
		username=request.POST ['username']
		password=request.POST ['password']
		email=request.POST ['email']
		if request.POST.get('isstatus'):

			myuser = User.objects.create_superuser(username=username, password=password,email=email)
			return redirect('admin_list')
		else:
			myuser = User.objects.create_user(username=username, password=password,email=email)
			return redirect('admin_list')
	return render(request, 'BC2_admin/auth/addadmin.html')


def admin_list(request):
	paginator = User.objects.all( ).order_by("id")
	#  获取用户数据 然后根据ID继续进行排序
	contacts1 = test(paginator, request.GET.get('page', 1))
	return render(request, 'BC2_admin/auth/admin_list.html',contacts1)

def editadmin(request):
	context={}
	uid=request.GET.get('uid')
	user=User.objects.get(id=uid)
	context['user']=user
	context ['Perlist'] = Group.objects.exclude(id__in=user.groups.all())
	if request.POST:
		uid=request.POST.get('uid')
		isstatus=request.POST.get('isstatus',None)
		if isstatus==None:
			user.is_superuser = False
		else:
			user.is_superuser = True
		username=request.POST.get('username')
		user.username=username
		
		authority=request.POST.get('authority',None)
		if authority:
			user.groups.clear()
			c=[authority]
			a = re.split(',+', c[0])
			for i in a:
				user.groups.add(i)
		user.save()
		return redirect('admin_list')
	return render(request, 'BC2_admin/auth/editadmin.html',context)



def admin_delete(request):
	data = { }
	uid = request.GET.get('upid')
	User.objects.get(id=uid).delete( )
	data ['erro'] = 1
	return JsonResponse({ 'bcak': 1 })
	