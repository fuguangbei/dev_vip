# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_userlabel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userlabel',
            options={'verbose_name': '\u7528\u6237\u6807\u7b7e', 'verbose_name_plural': '\u7528\u6237\u6807\u7b7e'},
        ),
        migrations.AlterModelOptions(
            name='userlabelcategory',
            options={'verbose_name': '\u7528\u6237\u6807\u7b7e\u79cd\u7c7b', 'verbose_name_plural': '\u7528\u6237\u6807\u7b7e\u79cd\u7c7b'},
        ),
        migrations.AlterField(
            model_name='userlabel',
            name='short',
            field=models.CharField(max_length=20, verbose_name='\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='userlabel',
            name='text',
            field=models.CharField(max_length=30, verbose_name='\u5168\u79f0'),
        ),
        migrations.AlterField(
            model_name='userlabelcategory',
            name='short',
            field=models.CharField(max_length=20, verbose_name='\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='userlabelcategory',
            name='text',
            field=models.CharField(max_length=30, verbose_name='\u5168\u79f0'),
        ),
    ]