# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0036_auto_20160602_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='concertorder',
            name='disneyorder_ptr',
        ),
        migrations.CreateModel(
            name='A',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='merchandise.Base')),
                ('alias', models.CharField(max_length=10)),
            ],
            bases=('merchandise.base',),
        ),
        migrations.DeleteModel(
            name='ConcertOrder',
        ),
    ]