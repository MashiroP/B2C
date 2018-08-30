from django.conf.urls import url

from .views import *
from .permission.add_admin import add_admin,admin_list

from .permission.admin_group import addgroup
urlpatterns = [
    url(r'^login',admin_login,name='admin_login'),
    url(r'^verifycode',verifycode,name='verifycode'),
    url(r'^Backstage', Backstage, name='Backstage'),#后台
    url(r'^BC2_User_modify',BC2_User_modify,name='BC2_User_modify'),# 用户数据
    url(r'^User_active',User_is_active,name='User_is_active'),# ajax 修改用户状态
    url(r'^User_detailed',BC2_User_detailed,name='BC2_User_detailed'),# 用户详情
    url(r'^User',BC2_admin_User,name='BC2_admin_User'),# 用户列表
    url(r'^dle_user',dle_user,name='dle_user'),# 删除用户
    url(r'^user_data',UP_user_data,name='UP_user_data'),#修改用户数据
    url(r'^BC2_admin_search',search,name='BC2_admin_search'),# 搜索
    url(r'^BC2_category',BC2_category,name='BC2_category'),# 添加商品类别
    url(r'^BC2_View_category',BC2_View_category,name='BC2_View_category'),# 商品类别查看
    url(r'^upload_data', upload_data, name='upload_data'),#  商品添加
    url(r'^BC2_admin_commodity', commodity_list, name='comm_list'),# 商品搜索
    url(r'^commodity_state', commodity_state, name='commodity_state'),# 商品修改
    url(r'^commodity_seve',commodity_seve,name='commodity_seve'),# 商品修改保存
	
	# 权限系统
	url(r'^add/admin',add_admin, name='add_admin'),
    url(r'^admin_list',admin_list,name='admin_list'),
    url(r'addgroup',addgroup,name='addgroup')
]