# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 07:00
from __future__ import unicode_literals

from django.db import migrations, models
import vip.utils


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0004_auto_20160519_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='disneyticket',
            name='cover',
            field=models.ImageField(null=True, upload_to=vip.utils.get_ticket_cover_upload_path, verbose_name='\u5c01\u9762\u56fe'),
        ),
    ]
