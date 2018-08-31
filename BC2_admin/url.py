from django.conf.urls import url

from .views import *
from .permission.add_admin import *

from .permission.admin_group import addgroup, listgroup, editgroup, group_delete
from .views.user_admin import *
from .views.goods import *


urlpatterns = [
    url(r'^login',admin_login,name='admin_login'),
    url(r'^verifycode',verifycode,name='verifycode'),
    url(r'^Backstage', Backstage, name='Backstage'),#后台
	
    url(r'^User/modify',User_modify,name='User_modify'),# 用户数据
    url(r'^User/active',User_is_active,name='User_is_active'),# ajax 修改用户状态
    url(r'^User/detailed',User_detailed,name='User_detailed'),# 用户详情
    url(r'^User/list',User_list,name='User_list'),# 用户列表
    url(r'^User/dle',User_dle,name='User_dle'),# 删除用户
    url(r'^User/data',UP_user_data,name='UP_user_data'),#修改用户数据
    url(r'^User/search',User_search,name='User_search'),# 搜索
	url(r'^User/add',User_add,name='User_add'),#用户添加
	
	
    url(r'^sort/add',sort_add,name='sort_add'),# 添加商品类别
    url(r'^sort/View',sort_View,name='sort_View'),# 商品类别查看
	
    url(r'^merchandise/add', merchandise_add_data, name='merchandise_add_data'),#  商品添加
	url(r'^merchandise/up_add', merchandise_add, name='merchandise_add'),#商品添加
    url(r'^merchandise/list', merchandise_list, name='merchandise_list'),# 商品列
    url(r'^merchandise/edit', merchandise_edit, name='merchandise_edit'),# 商品修改
    url(r'^merchandise/seve',merchandise_seve,name='merchandise_seve'),# 商品修改保存
	url(r'^merchandise/state',merchandise_state,name='merchandise_state'),#商品销售状态
	
	
	# 权限系统
	url(r'^admin/add',add_admin, name='add_admin'),
    url(r'^admin/list',admin_list,name='admin_list'),
    url(r'^admin/edit',editadmin,name='editadmin'),
    url(r'^admin/delete',admin_delete,name='admin_delete'),
    
    
    url(r'group/add',addgroup,name='addgroup'),
    url(r'group/list',listgroup,name='listgroup'),
    url(r'group/edit',editgroup,name='editgroup'),
    url(r'group_delete',group_delete,name='group_delete')
]