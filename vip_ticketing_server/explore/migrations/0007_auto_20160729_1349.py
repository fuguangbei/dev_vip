# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-29 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0006_post_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='\u89c6\u9891\u94fe\u63a5'),
        ),
    ]