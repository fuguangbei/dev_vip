# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0045_ticketorder_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketorder',
            name='contact',
            field=models.CharField(max_length=11, null=True, verbose_name='\u8054\u7cfb\u7535\u8bdd'),
        ),
    ]
