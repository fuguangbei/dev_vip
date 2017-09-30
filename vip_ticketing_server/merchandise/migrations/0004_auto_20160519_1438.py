# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0003_disneyticket_valid_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='IllustrationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='merchandise.Ticket')),
            ],
            options={
                'verbose_name': '\u63d2\u56fe',
                'verbose_name_plural': '\u63d2\u56fe',
            },
        ),
        migrations.AddField(
            model_name='disneyticket',
            name='purchace_notes',
            field=tinymce.models.HTMLField(null=True, verbose_name='\u8d2d\u4e70\u987b\u77e5'),
        ),
        migrations.AddField(
            model_name='disneyticket',
            name='ticket_intro',
            field=tinymce.models.HTMLField(null=True, verbose_name='\u5957\u9910\u4ecb\u7ecd'),
        ),
        migrations.AddField(
            model_name='disneyticket',
            name='vip_channel',
            field=tinymce.models.HTMLField(null=True, verbose_name='VIP\u901a\u9053'),
        ),
    ]