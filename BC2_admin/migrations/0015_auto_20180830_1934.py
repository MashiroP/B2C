# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-30 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BC2_admin', '0014_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('price', models.FloatField()),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BC2_admin.commodity')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='orderid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BC2_admin.Order'),
        ),
    ]
