# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-19 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_html', '0010_auto_20180819_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='uid',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
