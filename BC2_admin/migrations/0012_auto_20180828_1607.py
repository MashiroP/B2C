# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-28 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_admin', '0011_remove_profile_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Phone',
            field=models.CharField(max_length=13, null=True, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, default=0, max_length=2, null=True, verbose_name='性别'),
        ),
    ]