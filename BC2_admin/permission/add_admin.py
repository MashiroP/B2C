from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from ..extend.page import test

def add_admin(request):
	if request.POST:
		if request.POST.get('isstatus'):
			myuser = User.objects.create_superuser(request.POST ['username'], request.POST ['password'],is_staff=True)
			return redirect('')
		else:
			myuser = User.objects.create_user(request.POST ['username'], request.POST ['password'],is_staff=True)
			return redirect('')
	return render(request, 'BC2_admin/auth/addadmin.html')


def admin_list(request):
	paginator = User.objects.all( ).order_by("id")
	#  获取用户数据 然后根据ID继续进行排序
	contacts1 = test(paginator, request.GET.get('page', 1))
	return render(request, 'BC2_admin/auth/admin_list.html',contacts1)