# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0017_usermerchandise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermerchandise',
            name='likes',
            field=models.ManyToManyField(blank=True, to='merchandise.DisneyTicket', verbose_name='\u7528\u6237\u6536\u85cf'),
        ),
    ]
