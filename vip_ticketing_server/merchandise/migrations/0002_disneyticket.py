# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 05:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisneyTicket',
            fields=[
                ('ticket_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='merchandise.Ticket')),
            ],
            options={
                'verbose_name': '\u8fea\u58eb\u5c3c\u516c\u56ed\u95e8\u7968',
                'verbose_name_plural': '\u8fea\u58eb\u5c3c\u516c\u56ed\u95e8\u7968',
            },
            bases=('merchandise.ticket',),
        ),
    ]
