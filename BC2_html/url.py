
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',BC2_index,name='BC2_index'),
    url(r'BC2_login',BC2_login,name='BC2_login'),
    url(r'BC2_User',BC2_User,name='BC2_User'),
    url(r'test',test,name='test'),
    url(r'BC2_admin_index',BC2_admin_index,name='BC2_admin_index'),
    url(r'BC2_admin_User',BC2_admin_User,name='BC2_admin_User'),
    url(r'upload_data',upload_data,name='upload_data'),
    url(r'BC2_admin_commodity/([0-9]+)',commodity_list,name='comm_list'),
    url(r'so',sous,name='so'),



]
