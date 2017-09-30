# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0051_auto_20160608_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermerchandise',
            name='current_city',
            field=models.ForeignKey(default=1L, on_delete=django.db.models.deletion.CASCADE, to='merchandise.City', verbose_name='\u5f53\u524d\u57ce\u5e02'),
        ),
        migrations.AlterField(
            model_name='disneyorder',
            name='purchaser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disneyorders', to='merchandise.UserMerchandise', verbose_name='\u8d2d\u4e70\u4eba'),
        ),
    ]
