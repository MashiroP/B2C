from django.db import models
from django.contrib.auth.models import User



class profile(models.Model):
    
    name = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='姓名')
    user=models.CharField(max_length=20,verbose_name='账号')
    address = models.CharField(verbose_name='地址', max_length=100,null=True)
    Phone = models.CharField(verbose_name='电话号码', max_length=13,null=True)
    sex = models.CharField(verbose_name='性别',blank=True, default=0, max_length=2,null=True)
    active=models.BooleanField(default=False)
    headimage = models.ImageField(upload_to='./static/media/goods/', default='./static/media/img/1.jpg')

from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor_uploader.fields import RichTextUploadingField


class category(models.Model):
    category_father = models.CharField(max_length=10, verbose_name='父类别')
class category_Subcategory(models.Model):
    uid = models.ForeignKey(category, on_delete=models.CASCADE)
    Subgrade_name = models.CharField(max_length=20)


"""
类别：id，类别名称，父类别id号...
"""


class commodity(models.Model):
    Commodity_name = models.CharField(verbose_name='商品名字', max_length=50)
    describe = RichTextUploadingField( )
    Price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='商品价格')
    Stock = models.IntegerField(verbose_name='库存')
    Sales_volumes = models.IntegerField(verbose_name='销售数量', default=0)
    uid =models.ForeignKey(verbose_name='商品类别', to=category_Subcategory)
    Commodity_img = models.ImageField(verbose_name='商品图片', upload_to='./static/media/goods/')
    state = models.CharField(max_length=2, verbose_name='状态')
    """
    1新发布
    0  在售
    2 下架
    """
    commodity_delete = models.BooleanField(verbose_name='商品逻辑删除', default=0)
    Clicks = models.IntegerField(verbose_name='点击量', default=0)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
class Address(models.Model):
    
    # 用户 收货人 收货地址 收货电话  备注 是否默认地址
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    aname = models.CharField(max_length=10)
    ads = models.CharField(max_length=100)
    aphone = models.CharField(max_length=11)
    atags = models.CharField(max_length=10,null=True)
    isstatus = models.BooleanField(default=False)

class Order(models.Model):
    user_id = models.ForeignKey(to=User, to_field="id", on_delete=models.CASCADE)
    Consignee = models.CharField(max_length=10, verbose_name='收货人')
    Receiving_address = models.CharField(max_length=100, verbose_name='收货地址')
    phone = models.CharField(max_length=11, verbose_name='电话')
    Amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单价格')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    state = models.CharField(max_length=2, verbose_name='订单状态')
    
    
class cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    goos_id=models.ForeignKey(commodity, to_field="id", on_delete=models.CASCADE)
    num=models.IntegerField()
    
class OrderInfo(models.Model):
    orderid =  models.ForeignKey(to="Order", to_field="id")
    gid = models.ForeignKey(to="commodity", to_field="id")
    num  = models.IntegerField()
    price = models.FloatField()
