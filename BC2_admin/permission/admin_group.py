import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User,Group,Permission

from django.contrib.auth import login,logout

from django.contrib.auth.decorators import permission_required
from ..extend.page import test


def addgroup(request):
	context={}
	context['Perlist']=Permission.objects.exclude(name__istartswith='Can')
	if request.POST:
		g = Group()
		g.name = request.POST.get('title')
		g.save()
		prms = request.POST.getlist('authority', None)
		prms=prms[0]
		a=re.split(',+', prms)
		if prms:
			ps = Permission.objects.filter(id__in=a)
			g.permissions.set(ps)
			g.save( )
			return redirect('listgroup')
	return render(request, 'BC2_admin/auth/addgroup.html',context)

def listgroup(request):
	context={}
	context['Group']= Group.objects.all( )
	return render(request, 'BC2_admin/auth/group.html',context)

def editgroup(request):
	gid=request.GET.get('gid')
	a=Group.objects.get(id=gid)
	context = {}
	context ['Perlist'] = Permission.objects.exclude(name__istartswith='Can').exclude(id__in=a.permissions.all())
	context ['Group'] = a
	if request.POST:
		gid=request.POST.get('gid')
		title=request.POST.get('title')
		g = Group.objects.get(id=gid)
		g.permissions.clear()
		prms = request.POST.getlist('authority', None)
		prms = prms [0]
		a = re.split(',+', prms)
		ps = Permission.objects.filter(id__in=a)
		g.permissions.set(ps)
		g.name=title
		g.save()
		return redirect('listgroup')
	return render(request, 'BC2_admin/auth/editgroup.html', context)

def group_delete(request):
	data = { }
	uid = request.GET.get('upid')
	Group.objects.get(id=uid).delete()
	data ['erro'] = 1
	return JsonResponse({ 'bcak': 1 })