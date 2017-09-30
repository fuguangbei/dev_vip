# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 07:44
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
import vip.utils


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0008_auto_20160519_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disneyticket',
            name='cover',
        ),
        migrations.AddField(
            model_name='ticket',
            name='cover',
            field=models.ImageField(null=True, upload_to=vip.utils.get_ticket_cover_upload_path, verbose_name='\u5c01\u9762\u56fe'),
        ),
        migrations.AlterField(
            model_name='disneyticket',
            name='purchace_notes',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='\u8d2d\u4e70\u987b\u77e5'),
        ),
        migrations.AlterField(
            model_name='disneyticket',
            name='ticket_intro',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='\u5957\u9910\u4ecb\u7ecd'),
        ),
        migrations.AlterField(
            model_name='disneyticket',
            name='vip_channel',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='VIP\u901a\u9053'),
        ),
    ]
