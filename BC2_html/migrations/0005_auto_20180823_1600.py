# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-23 08:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_html', '0004_auto_20180823_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category_subcategory',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='commodity',
            name='Commodity_category',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='category',
        ),
        migrations.DeleteModel(
            name='category_Subcategory',
        ),
        migrations.DeleteModel(
            name='commodity',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
