# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0053_auto_20160615_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='concertorder',
            name='shipped',
            field=models.BooleanField(default=False, verbose_name='\u8ba2\u5355\u5df2\u5bc4\u51fa'),
        ),
        migrations.AddField(
            model_name='concertorder',
            name='shipping_code',
            field=models.CharField(blank=True, max_length=30, verbose_name='\u5feb\u9012\u5355\u53f7'),
        ),
        migrations.AddField(
            model_name='concertticket',
            name='seat',
            field=models.CharField(default='11\u53f7\u5305\u53a2 (\u4efb\u610f\u4f4d\u7f6e\u843d\u5ea7)', max_length=20, verbose_name='\u89c2\u6f14\u4f4d\u7f6e'),
        ),
    ]
