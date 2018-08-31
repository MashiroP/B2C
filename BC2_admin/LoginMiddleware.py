from django.shortcuts import render
from django.http import HttpResponse
import re
from django.core.urlresolvers import reverse


class LoginMiddleware:
	def __init__ (self, get_response):
		self.get_response = get_response
	
	# One-time configuration and initialization.
	
	def __call__ (self, request):
		
		# 检测当前的请求是否已经登录,如果已经登录,.则放行,如果未登录,则跳转到登录页
		
		# 获取当前用户的请求路径  /myadmin/开头  但不是 /myadmin/login/    /myadmin/vocde
		urllist = [reverse('admin_login'), reverse('verifycode')]
		# 判断是否进入了后台,并且不是进入登录页面
		if re.match('/admin/', request.path) and request.path not in urllist:
			
			# 检测session中是否存在 adminlogin的数据记录
			if request.session.get('AdminUser', '') == '':
				# 如果在session没有记录,则证明没有登录,跳转到登录页面
				return HttpResponse('<script>alert("请先登录");location.href="' + reverse('admin_login') + '";</script>')
		
		# 网站前台需要登录的地址
		urlarr = [
			# reverse('create'),
			# reverse('up_User'),
			# reverse('dxyz'),
			# reverse('dx'),
			# reverse('address'),
		]
		# 检测是否进入前台需要登录的请求
		if request.path in urlarr:
			# 检测是否登录
			if request.session.get('VipUser', '') == '':
				# 如果在session没有记录,则证明没有登录,跳转到登录页面
				return HttpResponse('<script>alert("请先登录");location.href="' + reverse(
					'myhome_login') + '?nextpath=' + request.path + '";</script>')
		
		# 其它情况  则放行
		response = self.get_response(request)
		return response