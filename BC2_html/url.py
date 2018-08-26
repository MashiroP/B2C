
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',BC2_index,name='BC2_index'),
    url(r'login',login,name='login'),
    url(r'BC2_User',BC2_User,name='BC2_User'),
    url(r'test',test,name='test'),
    url(r'BC2_admin_index',BC2_admin_index,name='BC2_admin_index'),
    url(r'create',create,name='create'),
    # url(r'User_updata',User_updata,name='User_updata'),
    url(r'up_User',up_User,name='up_User'),
    url(r'userLogout/',userLogout, name='logut'),
    url(r'dxyz',dxyz,name='dxyz'),
    url(r'dx',dx,name='dx'),
    url(r'yzmfs',yzmfs,name='yzmfs')

    
   
    # url(r'User_data',User_data,name='User_data')



]
