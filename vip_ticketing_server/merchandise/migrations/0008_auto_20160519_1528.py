# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0007_auto_20160519_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='available',
            field=models.IntegerField(default=0, verbose_name='\u5269\u4f59\u7968\u6570'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.IntegerField(null=True, verbose_name='\u4ef7\u683c'),
        ),
    ]
