# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0071_withdrawrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawrecord',
            name='withdraw_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u63d0\u73b0\u65f6\u95f4'),
        ),
    ]
