# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-22 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='momentscomments',
            name='corresponding_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moments_comments', to='moments.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='liked_count',
            field=models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570'),
        ),
    ]
