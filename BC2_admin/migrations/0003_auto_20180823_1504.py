# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-23 07:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_admin', '0002_auto_20180823_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Last_login',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='addtime',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
    ]
