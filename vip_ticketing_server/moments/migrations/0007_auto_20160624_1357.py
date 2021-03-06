# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 05:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moments', '0006_auto_20160624_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composed_moments', to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published_moments', to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u5e03\u4eba'),
        ),
    ]
