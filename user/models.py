from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user=models.CharField(max_length=20,verbose_name='账号')
    name=models.CharField(max_length=20,verbose_name='姓名')
    email = models.CharField(max_length=30)
    address = models.CharField(verbose_name='地址', max_length=100, blank=True)
    Phone = models.CharField(verbose_name='电话号码', max_length=13, blank=True)
    sex = models.CharField(verbose_name='性别',blank=True, default=0, max_length=2)
    headimage = models.ImageField(upload_to='./static/media/goods/', default='./static/media/img/1.jpg')
    addtime = models.DateTimeField(auto_now_add=True)
    password=models.CharField(max_length=200)
    state=models.CharField(max_length=1,verbose_name='状态',default=0)
    Last_login=models.DateTimeField(auto_now=True,null=True)
    """
    0普通
    1会员
    """


