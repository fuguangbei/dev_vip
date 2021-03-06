# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 08:31
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0013_disneyticket_vip_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='disneyticket',
            name='intro',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='\u5957\u9910\u4ecb\u7ecd'),
        ),
        migrations.AddField(
            model_name='disneyticket',
            name='purchase_notes',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='\u8d2d\u4e70\u987b\u77e5'),
        ),
        migrations.AlterField(
            model_name='disneyticket',
            name='vip_channel',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='VIP\u901a\u9053'),
        ),
    ]
