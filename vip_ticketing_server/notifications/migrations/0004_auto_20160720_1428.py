# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20160715_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='action',
            field=models.CharField(choices=[('Comment', '\u8bc4\u8bba\u4e86'), ('Share', '\u5206\u4eab\u4e86'), ('Register', '\u6ce8\u518c\u6210\u529f'), ('Like', '\u6536\u85cf\u4e86'), ('Dislike', '\u53d6\u6d88\u6536\u85cf\u4e86'), ('Approved', '\u901a\u8fc7\u5ba1\u6838'), ('Disapproved', '\u672a\u901a\u8fc7\u5ba1\u6838'), ('Favorite', '\u70b9\u8d5e\u4e86'), ('Unfavorite', '\u53d6\u6d88\u70b9\u8d5e\u4e86')], default='', max_length=20),
        ),
    ]
