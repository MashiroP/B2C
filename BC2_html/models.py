from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField


class category(models.Model):

    category_name=models.CharField(max_length=10,verbose_name='类别名称')
    uid=models.CharField(default='0',max_length=10)
    def __str__(self):
        return self.category_name


"""
类别：id，类别名称，父类别id号...
"""

class commodity(models.Model):
    Commodity_name=models.CharField(verbose_name='商品名字',max_length=50)
    describe=RichTextUploadingField()
    Price=models.DecimalField(max_digits=8, decimal_places=2,verbose_name='商品价格')
    Stock=models.IntegerField(verbose_name='库存')
    Sales_volumes=models.IntegerField(verbose_name='销售数量',default=0)
    Commodity_category=models.ManyToManyField(verbose_name='商品类别',to=category)
    Commodity_img=models.ImageField(verbose_name='商品图片',upload_to='./static/media/goods/')
    state=models.CharField(max_length=2,verbose_name='状态')
    """
    新发布
    在售
    下架
    """
    commodity_delete=models.BooleanField(verbose_name='商品逻辑删除',default=0)
    Clicks=models.IntegerField(verbose_name='点击量',default=0)
    addtime=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __str__(self):
        return self.Commodity_name




'''
商品：名称、类别id、厂家、图片、详情、单价、库存，销售量、点击量、添加时间、状态（新发布、在售、下架）
订单：id、 会员id、收货人、地址、电话、邮编、订单金额、添加时间、订单状态..
订单详情：订单id，商品id号，名称、单价、数量...
'''

class Order(models.Model):
    user_id=models.ForeignKey(to=User, to_field="id",on_delete=models.CASCADE)
    Consignee=models.CharField(max_length=10,verbose_name='收货人')
    Receiving_address=models.CharField(max_length=100,verbose_name='收货地址')
    phone=models.CharField(max_length=11,verbose_name='电话')
    zip_code=models.CharField(max_length=6,verbose_name='邮编')
    Amount=models.DecimalField(max_digits=10, decimal_places=2,verbose_name='订单价格')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    state = models.CharField(max_length=2, verbose_name='订单状态')


# class Order_details(models.Model):
#     订单id
#     商品id号