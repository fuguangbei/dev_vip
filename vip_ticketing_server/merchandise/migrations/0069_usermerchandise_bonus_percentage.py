# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0068_usermerchandise_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermerchandise',
            name='bonus_percentage',
            field=models.FloatField(choices=[(0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'), (0.4, '40%'), (0.5, '50%')], default=0, verbose_name='\u5206\u7ea2\u6bd4\u4f8b'),
        ),
    ]
