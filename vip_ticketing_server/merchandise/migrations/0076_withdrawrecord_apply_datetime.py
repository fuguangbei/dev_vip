# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0075_auto_20160712_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawrecord',
            name='apply_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u7533\u8bf7\u63d0\u73b0\u65f6\u95f4'),
        ),
    ]