
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',BC2_index,name='BC2_index'),
    url(r'login',login,name='login'),
    url(r'BC2_User',BC2_User,name='BC2_User'),
    url(r'BC2_admin_index',BC2_admin_index,name='BC2_admin_index'),
    url(r'create',create,name='create'),
    # url(r'User_updata',User_updata,name='User_updata'),
    url(r'up_User',up_User,name='up_User'),
    url(r'userLogout/',userLogout, name='logut'),
    url(r'dxyz',dxyz,name='dxyz'),
    url(r'dx',dx,name='dx'),
    url(r'yzmfs',yzmfs,name='yzmfs'),
    url(r'catalog_list',catalog_list,name='catalog_list'),
    url(r'commod/(?P<Uid>[0-9]+)',commod,name='commod'),
    url(r'lists',catalog_lists,name='lists'),
    url(r'look/cart', cart, name='cart'),
    url(r'add/cart',addcart,name='addcart'),
    

    
    
    

    
   
    # url(r'User_data',User_data,name='User_data')



]
