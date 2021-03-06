# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 06:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchandise', '0016_auto_20160521_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMerchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('likes', models.ManyToManyField(blank=True, null=True, to='merchandise.DisneyTicket', verbose_name='\u7528\u6237\u6536\u85cf')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u5546\u54c1\u884c\u4e3a',
                'verbose_name_plural': '\u7528\u6237\u5546\u54c1\u884c\u4e3a',
            },
        ),
    ]
