# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-16 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import vip.utils


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0019_auto_20160513_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=vip.utils.OverwriteStorage(), upload_to=vip.utils.get_avatar_upload_path, verbose_name='\u5934\u50cf'),
        ),
    ]