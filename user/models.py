from django.db import models
from django.contrib.auth.models import User




class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='账号')
    name=models.CharField(max_length=20,verbose_name='姓名')
    address = models.CharField(verbose_name='地址', max_length=50, blank=True)
    Phone = models.CharField(verbose_name='电话号码', max_length=13, blank=True)
    sex = models.CharField(verbose_name='性别',blank=True, default=0, max_length=2)
    BC2_admin=models.BooleanField(verbose_name='管理员',default=False)


    # headimage = models.ImageField(upload_to='./head_image', default='./head_image/1 (62).png')
    def __str__(self):
        return '<用户%s:昵称:%s>'%(self.user.username,self.name)
