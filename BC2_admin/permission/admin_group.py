from django.contrib.auth.models import User, Group
from django.shortcuts import render, HttpResponse, redirect
from ..extend.page import test
def addgroup(request):
	# g = Group( )
	# g.name = request.POST ['name']
	# # 执行添加
	# g.save( )
	
	return render(request, 'BC2_admin/auth/group.html',)