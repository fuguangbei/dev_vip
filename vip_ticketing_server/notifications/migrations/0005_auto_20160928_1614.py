# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-28 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20160720_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='content_type',
            field=models.CharField(choices=[('explore', '\u53d1\u73b0'), ('disney', '\u8fea\u58eb\u5c3c'), ('scenery', '\u666f\u533a'), ('moments', '\u5708\u5b50'), ('concert', '\u6f14\u5531\u4f1a'), ('aerospace', '\u5b87\u822a\u5957\u9910'), ('agent', '\u4ee3\u7406')], default='', max_length=10),
        ),
    ]
