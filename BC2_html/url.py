
from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^login',login,name='login'),
    url(r'^register',register,name='register'),

    url(r'^create',create,name='create'),
    
    url(r'up_User',up_User,name='up_User'),
    url(r'userLogout/',userLogout, name='logut'),

    url(r'SMS',SMS,name='SMS'),
    url(r'catalog_list',catalog_list,name='catalog_list'),
    url(r'commod/(?P<Uid>[0-9]+)',commod,name='commod'),
    url(r'lists',catalog_lists,name='lists'),
    
    url(r'look/cart', cart, name='cart'),
    url(r'add/cart',addcart,name='addcart'),
    url(r'cart_del',cart_del,name='cart_del'),
    url(r'cart_sc',cart_sc,name='cart_sc'),
    url(r'ddsc',ddsc,name='/ddsc',),
    
    url(r'address',address,name='address'),
    
    url(r'place_order',place_order,name='place_order'),
    url(r'test',test,name='test'),
    url(r'Personal_Center',Personal_Center,name='Personal_Center')
    
    


    
    
    

    
   
    # url(r'User_data',User_data,name='User_data')



]
