# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0055_auto_20160621_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermerchandise',
            name='current_city',
            field=models.ForeignKey(blank=True, default=1L, on_delete=django.db.models.deletion.CASCADE, to='merchandise.City', verbose_name='\u5f53\u524d\u57ce\u5e02'),
        ),
    ]
