# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-23 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, verbose_name='账号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('email', models.CharField(max_length=30)),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='地址')),
                ('Phone', models.CharField(blank=True, max_length=13, verbose_name='电话号码')),
                ('sex', models.CharField(blank=True, default=0, max_length=2, verbose_name='性别')),
                ('headimage', models.ImageField(default='./static/media/img/1.jpg', upload_to='./static/media/goods/')),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=200)),
                ('state', models.CharField(default=0, max_length=1, verbose_name='状态')),
                ('Last_login', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]