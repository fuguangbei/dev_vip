# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 09:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensitive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.CharField(blank=True, default='', max_length=7)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('added', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_user', to=settings.AUTH_USER_MODEL, verbose_name='\u6dfb\u52a0\u4eba')),
            ],
            options={
                'verbose_name': '\u654f\u611f\u8bcd',
                'verbose_name_plural': '\u654f\u611f\u8bcd',
            },
        ),
    ]