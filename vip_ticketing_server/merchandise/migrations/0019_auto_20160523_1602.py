# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0018_auto_20160523_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermerchandise',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='usermerchandise',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='usermerchandise',
            name='likes',
            field=models.ManyToManyField(blank=True, to='merchandise.Ticket', verbose_name='\u7528\u6237\u6536\u85cf\u95e8\u7968'),
        ),
    ]