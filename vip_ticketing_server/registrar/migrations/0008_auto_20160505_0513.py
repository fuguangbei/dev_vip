# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-05 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0007_vipuser_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipuser',
            name='pin_update_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='vipuser',
            name='pin',
            field=models.CharField(max_length=6, null=True, verbose_name='\u9a8c\u8bc1\u7801'),
        ),
    ]