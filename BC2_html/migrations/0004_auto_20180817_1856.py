# Generated by Django 2.0.5 on 2018-08-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_html', '0003_auto_20180817_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='Commodity_img',
            field=models.ImageField(upload_to='goods/', verbose_name='商品图片'),
        ),
    ]
