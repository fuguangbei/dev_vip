# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0022_auto_20160524_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermerchandise',
            name='concert_likes',
            field=models.ManyToManyField(blank=True, to='merchandise.ConcertTicket', verbose_name='\u5df2\u6536\u85cf\u6f14\u5531\u4f1a\u95e8\u7968'),
        ),
    ]