# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-06 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0015_auto_20160506_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipuser',
            name='promoter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registrar.VIPUser', verbose_name='\u63a8\u8350\u4eba'),
        ),
    ]