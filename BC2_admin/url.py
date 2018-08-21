from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^BC2_User_modify',BC2_User_modify,name='BC2_User_modify'),
    url(r'^User_is_active',User_is_active,name='User_is_active'),
    url(r'^BC2_User_detailed',BC2_User_detailed,name='BC2_User_detailed'),
    url(r'^dle_user',dle_user,name='dle_user')


]