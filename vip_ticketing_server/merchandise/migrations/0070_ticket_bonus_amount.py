# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0069_usermerchandise_bonus_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='bonus_amount',
            field=models.FloatField(default=0, verbose_name='\u63d0\u6210\u603b\u989d'),
        ),
    ]
