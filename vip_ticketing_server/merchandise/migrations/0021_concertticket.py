# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 09:32
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0020_auto_20160524_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcertTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='merchandise.Ticket')),
                ('time', models.DateField(blank=True, null=True, verbose_name='\u65f6\u95f4')),
                ('location', models.CharField(max_length=50, verbose_name='\u5730\u70b9')),
                ('vip_seating', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='VIP\u4e13\u5ea7')),
                ('purchase_notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='\u8d2d\u4e70\u987b\u77e5')),
                ('intro', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='\u6f14\u51fa\u4ecb\u7ecd')),
            ],
            options={
                'verbose_name': '\u6f14\u5531\u4f1a\u7968',
                'verbose_name_plural': '\u6f14\u5531\u4f1a\u7968',
            },
            bases=('merchandise.ticket',),
        ),
    ]
