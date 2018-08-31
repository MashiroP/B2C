# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-31 06:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
