# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 06:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0039_auto_20160602_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disneyorder',
            name='ticket_type',
        ),
        migrations.RemoveField(
            model_name='disneyorder',
            name='ticketorder_ptr',
        ),
        migrations.RemoveField(
            model_name='ticketorder',
            name='purchaser',
        ),
        migrations.DeleteModel(
            name='DisneyOrder',
        ),
        migrations.DeleteModel(
            name='TicketOrder',
        ),
    ]