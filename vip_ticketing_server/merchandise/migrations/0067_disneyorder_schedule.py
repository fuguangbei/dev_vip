# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0066_auto_20160704_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='disneyorder',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='merchandise.DisneySchedule', verbose_name='\u65e5\u671f'),
        ),
    ]